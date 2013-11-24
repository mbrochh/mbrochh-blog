Date: 2013-11-24
Title: Django And related_names
Tagline: Be A Good Citizen And Create Good Related Names
Slug: related-names
Category: Blog
Tags: python, django, djangoo-cms, rant

If you are a Django developer and if you create reusable apps, please
do everyone else a favour and be a good citizen and ALWAYS add related names to
all your foreign keys.

Why? For example, you cannot add Mezzanine and django-cms to the same project
because both apps have a Page model with a foreign key to Site and both apps
didn't provide a related name. Suckers!

When you finally add a related name, try to come up with name that is unlikely
to cause clashes with any other app out there. The safest way to do this is to
simply prepend your appname to the related name.

Bad example:

    #!python
    class Page(models.Model):
        site = models.ForeignKey(
            Site,
            related_name='pages',
        )

This doesn't help at all because it is very likely that some other app also
has a `Page` model and would also set the same related name, which would lead
to a clash again.

Good example:

    #!python
    class Page(models.Model):
        site = models.ForeignKey(
            Site,
            related_name='myapp_pages',
        )

This is good because it's quite unlikely that there will be another app which
has the same name as your app and has a Page model and uses this very same
foreign key and related name. Even if there is an app with the same name, you
would probably not be able to use both apps at the same time because they would 
have the same package name.
