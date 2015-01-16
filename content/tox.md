Date: 2015-01-20
Title: Maintaining Reusable Django Apps with Tox
Tagline: How to provide migrations for both, Django 1.6 & 1.7
Slug: tox
Category: Blog
Tags: python, django, database 

Django 1.7 was a [huge release](https://docs.djangoproject.com/en/1.7/releases/1.7/)
with tons of great new features.

One major change is that [South](http://south.readthedocs.org/en/latest/releasenotes/1.0.html#library-migration-path)
has been discontinued and Django now provides migrations in it's core.

This raises a problem for maintainers of reusable apps, [like me and my team](http://github.com/bitmazk/):

> How can we provide migrations for both, Django 1.6 & South and Django 1.7 & core migrations?

The good thing is that South as of version 1.0 will first look for a folder
called `south_migrations` and only afterwards search for the usual `migrations`
folder.  Therefore, you can simply rename your old `migrations` folder to
`south_migrations`.

Next you need to activate a second venv that has Django>1.7 installed and run
`./manage.py makemigrations appname`. This will create new initial migrations
using the new core migrations app.

Now you have two folders: `south_migrations` with your old migrations and
`migrations` with your new migrations.

Every time you make changes to your models, you have to activate the 1.6 venv
and run `./manage.py schemamigration appname --auto`, then activate the 1.7
venv and run `./manage.py makemigrations appname`. It might be a good idea to
create a fabric task `fab makemigrations` which takes care of everything.

If you are a good developer you will surely do Test Driven Development. In the
past I had given a PyCon Talk about [Test Driven Development with reusable Django apps](https://github.com/mbrochh/tdd-with-django-reusable-app).

In that talk I desribed how we execute our tests with a `runtests.py` so that
we don't need to setup a whole Django project for each reusable app. With
Django 1.7 there is a little problem, now: You will have `south` in your
`INSTALLED_APPS` setting but Django>1.7 does not allow that any more. As a
quick hack, you can simply add `south` only when the active Django version is
`<1.7`. Have a look at our [django-reusable-app-template](https://github.com/bitmazk/django-reusable-app-template/blob/master/template/package_name/tests/south_settings.py#L28)
for an example.

Finally, it would be really great to always run all tests against both
environments. This is where [tox](http://tox.readthedocs.org/en/latest/) enters 
the stage.

Your `tox.ini` should look like this:

    #!config
    [tox]
    envlist = py27-django{16,17}

    [testenv]
    usedevelop = True
    deps =
        django16: Django<1.7
        django17: Django>=1.7,<1.8
        -rtest_requirements.txt
    commands = {toxinidir}/VAR_PACKAGE_NAME/tests/runtests.py

The `envlist` setting defines a list of environments that tox should setup. We
can use variables here, so the `{16,17}` results in two environments with the
names `py27-django16` and `py27-django17`. In the `deps` setting we can make
use of those variables again and so we declare that in case of `django16` we
want to install `Django<1.7` and otherwise `Django>-1.7,<1.8`. Afterwards we
install our other `test_requirements.txt`. Behind the scenes this is the usual
call to `pip install -r test_requirements.txt`. Our reusable app also has a
`setup.py` with `install_requires`, thankfully, tox is smart enough to install
these dependencies as well.

All you have to do in order to run your tests is:

    #!py
    pip install tox
    tox

There is also a package called `detox` which claims to run the tests in
parallel but I couldn't get it up and running on OSX.
