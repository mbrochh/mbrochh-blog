Date: 2014-04-20
Title: Django Template Fragment Caching
Tagline: Speed up your site with Memcached and Template Fragment Caching
Slug: caching
Category: Blog
Tags: python, django 

Granted, when you look at the frontpage of [publishizer.com](https://publishizer.com)
you will say that it doesn't show much content, but even this simple site 
loads about 20 different partial templates and performs more than a hundred
database queries.

And what for? It rarely ever changes much. If we would get thousands of users,
we would waste tens of thousands of CPU cycles and IO operations on our
webserver, which would ultimately cost us a lot of money. In order to prevent
this, I recently had a closer look at Django's powerful caching framework.

## 1. Install Memcached

Luckily, on our Webfaction servers, Memcached is already installed. I can't
remember how I installed it on OSX, but I guess I just ran
`brew install memcached`

## 2. Start & Stop Memcached

In order to start Memcached, just run:

    #!bash
    memcached -d -m 50 -s $HOME/memcached.sock -P $HOME/memcached.pid

This will start it in daemon mode and reserve 50MB of space for your cache.

In order to stop Memcached, just run:

    #!bash
    kill $(cat $HOME/memcached.pid)

I created [Fabric](http://www.fabfile.org/) tasks for this so that I can
restart memcached locally or on our servers easily and added this as one step
at the end of our deployment script.

## 3. Add cache settings to your Django settings

Now we setup the whole caching magic. I put this into my `local_settings.py`
because every developer might want to play around with this and most of the
time you would deactivate caching during local development but of course you
want to activate it on the production server.

    #!py
    # [... rest of your local_settings.py]

    CACHE = True

    # Start memcached via:
    # memcached -d -m 50 -s $HOME/memcached.sock -P $HOME/memcached.pid
    # Stop it via:
    # kill $(cat $HOME/memcached.pid)
    if CACHE:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                'LOCATION': 'unix:/Users/username/memcached.sock',
            },
        }
        TEMPLATE_LOADERS = (
            ('django.template.loaders.cached.Loader', (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            )),
        )
        SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
        CACHE_MIDDLEWARE_KEY_PREFIX = 'yourproject_'
    else:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        }
        TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            'django.template.loaders.eggs.Loader',
        )

First of all, make sure to change the `LOCATION` setting and set `username` to
your username. If you don't want to save the socket in your home folder, you
might also want to change the path.

Secondly change the `CACHE_MIDDLEWARE_KEY_PREFIX` to your projectname.

Note that we are also using cached template loaders here. If you follow the 
DRY principle, you will quickly have dozens or even hundreds of small partial
templates. This will create quite some load on your CPU/disk because for each
request Django tries to find the template file for each partial template on the
hard disk. Usually your template locations will never change, so this is a safe
thing to put into a cache. 

With these settings, you can just set `CACHE = False` when you do local
development. If you don't set this to `False`, you will have to restart
memcached every time you change something in your templates.

## 4. Create some cache utils

If you are on Django 1.4, you will need a little helper class. Put this into 
a file `cache_utils.py`:

    #!py
    from django.core.cache import cache
    from django.utils.hashcompat import md5_constructor
    from django.utils.http import urlquote

    def invalidate_template_fragment(fragment_name, *variables):
        args = md5_constructor(u':'.join([urlquote(var) for var in variables]))
        cache_key = 'template.cache.%s.%s' % (fragment_name, args.hexdigest())
        cache.delete(cache_key)

For Django 1.5 you can reuse the method for creating the fragment key:

    #!py
    from django.core.cache import cache
    from django.core.cache.utils import make_template_fragment_key

    def invalidate_template_fragment(fragment_name, *variables):
        cache_key = make_template_fragment_key(
            fragment_name, vary_on=variables) 
        cache.delete(cache_key)

## 5. Use django-debug-toolbar-template-timings

Any serious Django developer should use the [django-debug-toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar).
If you have that installed, make sure that you also use the plugin
[django-debug-toolbar-template-timings](https://github.com/orf/django-debug-toolbar-template-timings).

This will show you the CPU time needed for each of your partial templates and
makes it super easy to identify the parts in your template that take the most
time to render.

## 6. Use template fragment caching

Some parts of your templates are not good candidates for caching, because they
change often, for example the header of your site might contain the name of
the logged in user and the main menu might be different for different kinds
of users. While technically possible, I think this is not a good idea to cache.
If you have millions of users it would mean that you need to add millions of
template fragments into the cache, one for each user. I guess that would eat up
all your RAM in no time.

If you have parts that don't change often and are the same for every user,
those are great candidates for caching.

It looks like this:

    #!html
    {% load cache %}
    {% cache 300 ebook_home_html %}
        {% include "ebook/partials/ebook_home.html" %}
    {% endcache %}

This is the part on publishizer.com that renders the grid of ebook campaigns.
It looks the same for every user and it rarely changes (only when someone
preorders a book or when a campaign ends).

I set the cache time to 5 minutes and gave it the cache key `ebook_home_html`.

This improved the load time of our frontpage from 1800ms to 120ms.

## 7. Manually invalidate caches

Five minutes is cool but what if a campaign ends or a user makes a preorder?
It would be cool to always show up to date data on the frontpage. For this
reason we created the `cache_utils.py` module as desribed above. It allows us
to invalidate the cache whenever we definitely know that something has changed.

It's usage could simply look like this:

    #!py
    def payment_completed_handler(sender, transaction, **kwargs):
        """Sends the thank-you email when a payment is completed."""
        invalidate_template_fragment('ebook_home_html')
        # ... rest of the function

So whenever someone makes a payment, we invalidate the cache.

That's it. Hopefully at some happy point in the future, this approach will no
longer be good enough, because we might have thousands of campaigns at the same
time and dozens of preorders per second. This would mean that the cache would
constantly be invalidated and therefore become pointless. However, this could
easily be solved. Instead of caching the whole frontpage, I could go one level
deeper and cache the individual rendered campaign cards. We would never show
more than a few dozen of those cards on the frontpage anyways, so having those
in the cache would be feasible.

Dozens of preorders per second. Ah well... one can only dream...
