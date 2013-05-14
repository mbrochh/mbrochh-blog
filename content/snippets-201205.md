Date: 2012-05-30
Title: Snippets of Mai 2012
Slug: snippets-201205
Category: Blog
Tags: snippets
status: draft

This is my third post in a series of (almost) monthly posts about small bits
and pieces of wisdom that amazed me. You can find the last post here:
[Snippets of April 2012](http://martinbrochhaus.com/2012/04/snippets-201204.html)

# git aliases

# git defaults
http://jk.gs/git-config.html

    [push]
    default = upstream
# factory_boy
# access django from parallels

    ::sh
    ifconfig -a
    ./manage.py runserver 192.168.0.10:8000

In Parallels, start IE and browse to http://192.168.0.10:8000

# Chinese translations in Django

http://stackoverflow.com/questions/7728977/django-how-to-add-chinese-support-to-the-application

Put ``zh-cn`` in your settings.py but run ``makemessages -l zh_CN``


# Replacing a field on a form

Let's assume:

    ::py
    class FooBar(models.Model):
        foo = models.IntegerField()
        bar = models.IntegerField()

    class FormBar(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(FormBar, self).__init__(*args, **kwargs)
            self.fields['bar'] = MyCustomIntegerField()

    class FormFooBar(FormBar):
        class Meta:
            model = FooBar

Usually we would instantiate the form ``FormFooBar`` which gets all it's fields
created by the model. However, in the superclass, ``FormBar`` we would like
to replace the automatically created field ``bar`` by a custom implementation
of the IntegerField which would display a different value than the one that
is actually saved on the instance.

The code above would still show the value from the instance. It took me quite
some time to find out that we also need to add this line after:

    ::py
    ...
    self.fields['bar'] = MyCustomIntegerField()
    self.initial['bar'] = my_custom_calue


# Django and Sphinx autodoc
* add the following to conf.py

    ::py
    sys.path.insert(0, os.path.abspath('../website/webapps/django/'))
    # setup django
    import settings
    from django.core.management import setup_environ
    setup_environ(settings)

* change this in Makefile

    ::sh
    SPHINXBUILD   = python $(shell which sphinx-build)

* run sphinx-apidoc -f -o api ../website/webapps/django/project

# django-cms dumpdata placeholder

* do not name your placeholders '01 content', better '01_content'

# great content

* http://www.youtube.com/watch?v=bf7BXwVeyWw
  Pretty cool explanation of the status quo in cosmology. The idea of a future
  civilisation that will no longer be able to see any other galaxy due to red
  shift is just mind blowing.
