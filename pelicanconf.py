#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

THEME = '/Users/martin/Forks/pelican-themes/notmyidea-cms'

AUTHOR = u'Martin Brochhaus'
SITENAME = u'martinbrochhaus.com'
SITEURL = ''

TIMEZONE = 'Asia/Singapore'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)
LINKS = ()

# Social widget
SOCIAL = (
    ('Github', 'https://github.com/mbrochh'),
    ('Google Plus', 'https://plus.google.com/101162916953876296847/about'),
    ('Twitter', 'https://twitter.com/mbrochh'),
    ('Facebook', 'https://facebook.com/mbrochh'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

FILES_TO_COPY = (
    ('extra/CNAME', 'CNAME'),
)
