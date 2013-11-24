Date: 2013-11-24
Title: Django And related_names
Tagline: Be A Good Citizen And Create Good Related Names
Slug: cmsplugins
Category: Blog
Tags: python, django, djangoo-cms, rant

I just learned a lesson the hard way: Don't add a `cms_plugins.py` file to
your reusable app! Create a separate app for the apphook and cms plugin
instead.

Almost [all our apps](https://github.com/bitmazk/) play nicely with django-cms
and so we didn't think much when adding `cms_apps.py` and `cms_plugins.py`
files to all our reusable apps during the last two years.

In hindsight, this was an extremely bad decision. We have a new customer now
who is using Mezzanine instead of django-cms (do yourself a favour and avoid
Mezzanine at all cost). When we wanted to re-use our
[django-frequently](https://github.com/bitmazk/django-frequently) in that
project, we realised that django-frequently requires django-cms but you can't
install django-cms next to Mezzanine. This is because both apps have a Page
model with a foreign key to Django's Site model and no `related_name` attribute
set on that field.

## Lesson Learned: Always Add related_names

So yea, if you are a Django developer and if you create reusable apps, please
do everyone else a favor and be a good citizen and ALWAYS add related names to
all your foreign keys.

And when you do so, try to come up with a related name that is unlikely to
cause clashes with any other app out there.

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

But that's not really the point of this post.
