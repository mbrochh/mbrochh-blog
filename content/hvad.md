Date: 2013-10-30
Title: Migrating Apps from simple-translation to django-hvad
Tagline: Another Lessons Learned While Getting Ready for django-cms 3.0
Slug: hvad
Category: Blog
Tags: python, django, django-cms, howto

This is the second post in a small [series](|filename|djangocms3.md) about
problems that might occur when migrating from django-cms 2 to 3.

In my first post I described [how to get rid of the
M2MPlaceholderField](|filename|m2mplaceholderfield.md).

This post will deal with the migration from simple-translation to
[django-hvad](https://github.com/KristianOellegaard/django-hvad).

As mentioned in my first post, two years ago we made the decision to use
simple-translation for [all our app](https://github.com/bitmazk/) because
cmsplugin-blog was using it as well.

It turns out that this was a bad decision, because django-cms 3 now makes
great use of django-hvad. Besides, django-hvad has a much cleaner API than
simple-translation, so it is about time to get rid of the latter.

The migration should be straight forward:

1. Add changes to model and admin needed by hvad
2. Create a datamigration to copy all content from simple-translation to hvad
3. Remove simple-translation model

## The Problems

### 1. You cannot use translated fields in the admin's list_display

Let's say your model has a translated field named ``title`` and in your model
admin you want to do something like ``list_display = ['title', ]`` then you
would get the following error:

    WrongManager at /en/admin/multilingual_news/newsentry/
    To access translated fields like 'title' from an untranslated model,
    you must use a translation aware manager,
    you can get one using nani.utils.get_translation_aware_manager.

This is a deep problem with Django's admin implementation and there is an
[issue](https://github.com/KristianOellegaard/django-hvad/issues/98) for this.

You can solve this with a workaround by creating your admin class like so:

    #!python
    class NewsEntryAdmin(TranslatableAdmin):
        list_display = ['get_title', ]

        def get_title(self, obj):
            return obj.title
        get_title.short_description = _('Title')

## 2. You still need PlaceholderAdmin

This one is not really a problem but it took me by surprise. In django-cms 3
we don't need the placeholder fields to be in the admin any more because we
edit the placeholders on the frontend only. So when I followed the hvad docs
I implemented my admin class so that it only inherits from
``TranslatableAdmin``, which worked well with a djangoo-cms 3 project.

However, you will want your app to be backwards compatible and therefore you
will want to keep the placeholder fields in your admin. In order to do that,
your admin class must of course inherit from ``PlaceholderAdmin``, otherwise
you will get this error when you access an objects change admin in a django-cms
2 project:

    <lambda>() takes exactly 1 argument (2 given)

## The Migration

Lets say your model that uses simple-translation looks like this:

    #!python
    class NewsEntry():
        pub_date = models.DateTimeField()

    class NewsEntryTrans(models.Model):
        title = models.CharField()

        # needed by simple-translation
        entry = models.ForeignKey(NewsEntry)
        language = models.CharField()

I hope that you didn't name your translation model ``NewsEntryTranslation``
because that would be the same name that hvad would try to use. Thankfully I
haven't had that problem yet, but if I had, I would have to rename the
translation table first. South can handle
[renaming a Django model](http://stackoverflow.com/questions/2862979/easiest-way-to-rename-a-model-using-django-south).

The first thing we will do is to add the fields from the translation model to
the original model, but this time following the
[hvad docs](http://django-hvad.readthedocs.org/en/latest/public/quickstart.html):

    #!python
    from hvad.models import TranslatableModel, TranslatedFields

    class NewsEntry(TranslatableModel):
        pub_date = models.DateTimeField()

        translations = TranslatedFields(
            title=models.CharField(),
        )

    class NewsEntryTrans(models.Model):
        ...

Create a South schemamigration for this. Diretly after that also create a
South datamigration, which should look like this:

    #!python
    class Migration(DataMigration):
        def forwards(self, orm):
            for entry_trans in orm.NewsEntryTrans.objects.all():
                entry = NewsEntry.objects.get(pk=entry_trans.entry.pk)
                entry.translate(entry_trans.language)
                entry.title = entry_trans.title
                entry.save()

Finally you can delete the ``NewsEntryTrans`` model and create a South
schemamigration for this as well. Of course you will have to make some changes
to your templates, because you will not need the ``simpletranslation_tags``
any more and just access ``object.title`` in your templates, which is awesome!
