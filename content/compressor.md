Date: 2014-04-19
Title: Django-compressor and Amazon S3
Tagline: Use local offline compression and serve compressed files via Amazon S3 
Slug: compressor
Category: Blog
Tags: python, django, amazon

As described in my [last post]({filename}s3.md) we are serving the media files
that are uploaded by our users via Amazon S3. We do not serve our static files
via S3 because it slows down our deployment. `./manage.py collectstatic` would
currently find more than 280 files and it would take forever to upload them
all to Amazon. Most of these static files are even completely unrelated to
our projects - they are images, style sheets and javascript files for the
Django admin or for django-cms. It is not crucial for us to serve those files
in the fastest way possible and only our admins will ever see those files, so
traffic is also not an issue.

There are two static files, though, that get served to all our users and
therefore should be hosted on S3: Our compressed CSS and JS files.

We use [django-compressor](https://github.com/django-compressor/django-compressor)
for compression.

The problem is: When you tell compressor to use S3, it will also search for the
source that should be compressed on S3. This, of course, will be futile because
I don't upload all my static files to S3. With a bit of tinkering and
consulting Stackoverflow I found a solution for this.

## 1. Create a custom css filter

First of all you will need a custom CssAbsoluteFilter because the original one
does not work when you have `DEBUG=True` and it would insert the Amazon S3 URL
everywhere. You don't want that because your static files are not hosted on S3.
You want it to insert your website's full domain instead.

Here is a snippet that overrides some methods of the origingal
CssAbsoluteFilter and addresses both problems. Make sure that you have a
`FULL_DOMAIN = 'https://example.com'` setting in your `local_settings.py`.
Put this into `yourproject/compress_filters.py`:

    #!py
    from django.conf import settings
    from compressor.filters.css_default import CssAbsoluteFilter
    from compressor.utils import staticfiles

    class CustomCssAbsoluteFilter(CssAbsoluteFilter):
        def __init__(self, *args, **kwargs):
            super(CustomCssAbsoluteFilter, self).__init__(*args, **kwargs)
            self.url = '%s%s' % (settings.FULL_DOMAIN, settings.STATIC_URL)
            self.url_path = self.url

        def find(self, basename):
            # The line below is the original line.  I removed settings.DEBUG.
            # if settings.DEBUG and basename and staticfiles.finders:
            if basename and staticfiles.finders:
                return staticfiles.finders.find(basename)


## 2. Create a custom S3BotoStorage backend

Next you need to make sure that django-storages searches for the source files
that should be compressed on the local filesystem but uploads the compressed
files to Amazon S3. Put this into a file `yourproject/s3utils.py`:

    #!py
    from django.core.files.storage import get_storage_class
    from storages.backends.s3boto import S3BotoStorage

    class CachedS3BotoStorage(S3BotoStorage):
        def __init__(self, *args, **kwargs):
            super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
            self.local_storage = get_storage_class(
                'compressor.storage.CompressorFileStorage')()

        def save(self, name, content):
            name = super(CachedS3BotoStorage, self).save(name, content)
            self.local_storage._save(name, content)
            return name


    CompressorS3BotoStorage = lambda: CachedS3BotoStorage(location='compressor')
    MediaRootS3BotoStorage = lambda: S3BotoStorage(location='media')

By the way, in my buckets on Amazon I have subfolders. One `media` folder for
the media files uploaded by our users and one `compressor` folder for the
compressed files uploaded by django-compressor. Those two lines with `lambda`
at the bottom make sure that I can use my backends and have the files uploaded
to the correct subfolder.

## 3. Setting everything up

First of all, set some Django settings for compressor:

    #!py
    COMPRESS_PARSER = 'compressor.parser.HtmlParser'
    COMPRESS_CSS_FILTERS = [
        'myproject.compress_filters.CustomCssAbsoluteFilter',
    ]
    COMPRESS_ENABLED = True

Secondly, set `SOMPRESS_STORAGE` in your `local_settings.py`:

    #!py
    if USE_S3:
        DEFAULT_FILE_STORAGE = 'myproject.s3utils.MediaRootS3BotoStorage'
        THUMBNAIL_DEFAULT_STORAGE = 'myproject.s3utils.MediaRootS3BotoStorage'
        MEDIA_URL = S3_URL + '/media/'
        COMPRESS_STORAGE = 'myproject.s3utils.CompressorS3BotoStorage'

In my last post I had set everything up in such a way so that I can disable
S3 usage simply by setting `USE_S3 = False` in my `local_settings.py`.
Therefore the new `COMPRESS_STORAGE` setting is added within the `if USE_S3`
if-clause.

## 4. Change your deployment workflow

Whenever you run a deployment (I hope you use [Fabric](http://fabric.readthedocs.org/en/latest/))
you must make sure to call `./manage.py compress --force`. We do this after
the collectstatic step and before the `touch wsgi` step.

That's all. From now on, compressor will search the source files for
compression on the server's local storage and then upload only the compressed
files to Amazon S3.

Note: In this setup you will want to set `COMPRESS_ENABLED = False` during
local development, otherwise it will be hard to debug JS or CSS issues. If you
set it to `True` you must run `./manage.py collectstatic` every time you change
a CSS or JS file.
