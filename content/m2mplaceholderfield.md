Date: 2013-10-28
Title: Getting Rid of M2MPlaceholderFields
Tagline: Because You Can't Use Them With django-cms 3 Any More
Slug: m2mplaceholderfields
Category: Blog
Tags: python, django, django-cms, howto

In my [last post](|filename|/djangocms3.md) I gave an overview over some 
hurdles I had to overcome in order to migrate
[django-multilingual-news](https://github.com/bitmazk/django-multilingual-news).
to django-cms 3.

We can't use the M2MPLaceholderAdmin any more because it uses a widget that
no longer exists in django-cms 3. We also don't need to use this any more
because in django-cms 3 we are not supposed to manipulate PlaceholderFields
in the Django admin - we are supposed to edit them via frontend editing.

## The Plan 

In my app, the Usage of the M2MPlaceholderField looks as follows:

    #!python
    class NewsEntry(models.Model):
        # ...
        placeholders = M2MPlaceholderField(
            actions=SimpleTranslationPlaceholderActions(),
            placeholders=('excerpt', 'content'),
        )

You can see that via the ``placeholders`` parameter, we defined the number
of placeholders that we want and their slotnames.

The idea for a migration is straightforward:

1. On the model that has the M2MPlaceholderField, we add new PlaceholderFields:
   One for each slotname that we had on the M2MPlaceholderField
2. Now we add a datamigration which creates new Placholders for these
   new fields and moves all the plugins from the old placeholders to the new
   ones.
3. Finally we can remove the old M2MPlaceholder field.

Therefore, after the migration, the model should look like this:

    #!python
    class NewsEntry(models.Model):
        excerpt = PlaceholderField(
            slotname='multilingnual_news_excerpt',
            related_name='multilingual_news_excerpts',
            blank=True, null=True,
        )

        content = PlaceholderField(
            slotname='multilingnual_news_content',
            related_name='multilingual_news_contents',
            blank=True, null=True,
        )

## The Problems

This sounds trivial at first, but in fact it took me quite a while to figure
out because there is a lot of magic involved in the PlaceholderFields that will
not be reflected inside the South datamigration. You will face two issues:

### 1. You can't call object.placeholders.all()

In the datamigration, we would usually iterate over all NewsEntry objects
and then migrate their placeholders:

    #!python
    for entry in orm.NewsEntry.objects.all():
        try:
            placeholder = entry.placeholder.get(slot='excerpt')
        except ObjectDoesNotExist
            pass
        if placeholder:
            # create new placeholder here and copy all cmsplugins

The pitfall here is: At first this works. But when you add the final migration
where you delete the M2MPlaceholderField, this stops working.

When trying to get the placeholder, you will get the error that ``newsentry``
is no available field on the Placeholder model. This suggests, that
``entry.placeholder`` tries to call something like
``Placeholder.newsentry_set.all()`` internally. I looked at it in the debugger
and indeed, ``Placeholder.newsentry_set`` does not exist.

This is (almost) logical: In the last step, we would remove the 
M2MPlaceholderField, therefore, when starting Django, it would not find any
relation between Placeholder and NewsEntry and therefore it would not
add ``newsentry_set`` to the Placeholder model. Creating the migration
with ``--freeze`` didn't help as well, therefore South doesn't seem to
be able to create those backwards relation fields, even on frozen models.
Bummer.

### 2. You can't assign the placeholder objects

At first I thought, I will just get the existing placeholder objects and then
just re-assign them to the new PlaceholderFields like so:

    #!python
    placeholder = entry.placeholders.get(slot='excerpt') 
    entry.excerpt = placeholder
    entry.save()

If only life would be that simple!

Turns out this wasn't possible. For some weird reason the placeholders that
can be assigned to model fields of type ``PlaceholderField`` must be of type
``<cms.models.Placeholder>`` but the placeholders that we get from the
``M2MPlaceholderField`` are of type 
``<cms.models.placeholderfield.Placeholder>``.

## The Solution

The code I came up with in my datamigration looks like this (part 1):

    #!python
    def migrate_placeholder(self, orm, entry, old_slot, new_slot, new_field):
            placeholder = None
            try:
                placeholder_m2m_object = entry.placeholders.through.objects.get(
                    newsentry=entry, placeholder__slot=old_slot)
                placeholder = placeholder_m2m_object.placeholder
            except ObjectDoesNotExist:
                pass

I learned something cool here: When using many to many relationships, Django
will magically create intermediary relation tables. I always knew this but I
did not know that you can easily query those tables via the ORM and you will
get back nice Django models.

So since I can't just call ``entry.placeholders.get()`` I worked around this
by getting the m2m_objects and retrieving the Placeholder object from those.

This solved Problem #1.

The rest of my snippet looks like this:

    #!python
    if placeholder:
        placeholder_cls = orm['cms.Placeholder']
        new_placeholder = placeholder_cls.objects.create(slot=new_slot)
        for plugin in placeholder.get_plugins():
            plugin.placeholder_id = new_placeholder.pk
            plugin.save()
        setattr(entry, new_field, new_placeholder)
        entry.save()
        try:
            newsentry_placeholder.delete()
            placeholder.delete()
        except ObjectDoesNotExist:
            pass

First I make sure to create a ``new_placeholder`` that is of type 
``<cms.models.Placeholder>`` (so that we can assign it to the new fields on
the entry objects), then I take all plugins from the old placeholder
and change their ``placeholder_id`` to the new placeholder.

This solved Problem #2.

The final datamigration script looks like this:

    #!python
    class Migration(DataMigration):

        def migrate_placeholder(self, orm, entry, old_slot, new_slot, new_field):
                placeholder = None

                try:
                    newsentry_placeholder = entry.placeholders.through.objects.get(
                        newsentry=entry, placeholder__slot=old_slot)
                    placeholder = newsentry_placeholder.placeholder
                except ObjectDoesNotExist:
                    pass
                if placeholder:
                    placeholder_cls = orm['cms.Placeholder']
                    new_placeholder = placeholder_cls.objects.create(slot=new_slot)
                    for plugin in placeholder.get_plugins():
                        plugin.placeholder_id = new_placeholder.pk
                        plugin.save()
                    setattr(entry, new_field, new_placeholder)
                    entry.save()
                    try:
                        newsentry_placeholder.delete()
                        placeholder.delete()
                    except ObjectDoesNotExist:
                        pass

        def forwards(self, orm):
            "Write your forwards methods here."
            # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
            for entry in orm['multilingual_news.NewsEntry'].objects.all():
                self.migrate_placeholder(
                    orm, entry, 'excerpt', 'multilingual_news_excerpt', 'excerpt')
                self.migrate_placeholder(
                    orm, entry, 'content', 'multilingual_news_content', 'content')

One note about the slot names: You can see that I changed the slot names from
``excerpt`` to ``multilingual_news_excerpt`` and likewise from ``content`` to
``multilingual_news_content``. This makes sense because the slot names allow
you to define which plugins should be allowed in this slot. Just ``content`` is
quite a generic slot name which might be used by many differnet apps, so it is
better to create proper slot names here that can uniquely identify your app's
placeholder field. 

I ran this migration against a new Django 1.5 / django-cms 3 project and it
worked. I also ran it against an existing Django 1.4 / django-cms 2.3 project
and all existing cmsplugins showed up nicely in the new PlaceholderFields.

Life is good.
