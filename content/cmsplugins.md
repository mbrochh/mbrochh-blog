Date: 2013-11-24
Title: Isolate Django-CMS Plugins
Tagline: Howto Migrate Your Plugins Into Separate Apps 
Slug: cmsplugins
Category: Blog
Tags: python, django, djangoo-cms, howto
Status: draft

I just learned a lesson the hard way: Don't add a `cms_plugins.py` file to
your reusable app! Create a separate app for the apphook and cms plugin
instead.

Almost [all our apps](https://github.com/bitmazk/) play nicely with django-cms
and so we didn't think much when adding `cms_apps.py` and `cms_plugins.py`
files to all our reusable apps during the last two years.

In hindsight, this was an extremely bad decision. We have a new customer now
who is using Mezzanine instead of django-cms (do yourself a favour and avoid
Mezzanine at all cost). 

When we wanted to re-use our [django-frequently](https://github.com/bitmazk/django-frequently) 
in that project, we realised that django-frequently requires django-cms but you
can't install django-cms next to Mezzanine for reasons unrelated to this post.

Of course, django-frequently doesn't really need django-cms if you don't want
to use the apphook or the cmsplugin.
