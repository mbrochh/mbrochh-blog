Date: 2013-10-27
Title: Migrating to django-cms 3
Tagline: The Challenges You Might Face When Migrating Apps To django-cms 3 
Slug: djangocms3
Category: Blog
Tags: python, django, django-cms, howto 

You might have heard it: [django-cms 3](https://www.django-cms.org/en/) is in
beta now, so a final release might be released soon. For a long time we had
used [cmsplugin-blog](https://github.com/fivethreeo/cmsplugin-blog) with all
our django-cms installations. Unfortunately it was lacking many features that
we always needed, didn't have much code coverage and didn't use class based
views, so we created
[django-multilingual-news](https://github.com/bitmazk/django-multilingual-news).

The last few days I tried to add multilingual-news to a new django-cms 3
project and of course everything failed miserably. I have since spent many
hours, trying to figure out how to migrate multilingual-news so that it will
remain backwards compatible with django-cms>=2.3. I thought it might be a good
idea to write this down because I have to repeat this process for a ton of
apps. It might be helpful to others and a bit of peer review probably can't
hurt - maybe I'm doing things overly complicated, after all. 

## The challenges

### 1. M2MPlaceholderAdmin is no more

cmsplugin-blog has this fancy
[M2MPlaceholderAdmin](https://github.com/fivethreeo/cmsplugin-blog/blob/develop/cmsplugin_blog/admin.py#L24).
When we created multilingual-news we [copied that admin](https://github.com/bitmazk/django-multilingual-news/blob/master/multilingual_news/admin.py#L19).
The problem is, that this admin makes use of the
[PlaceholderPluginEditorWiget](https://github.com/bitmazk/django-multilingual-news/blob/master/multilingual_news/admin.py#L37)
which no longer exists in django-cms 3.

It gets worse: The very
[M2MPlaceholderField](https://github.com/fivethreeo/djangocms-utils/blob/master/djangocms_utils/fields.py#L30)
comes from [djangocms-utils](https://github.com/fivethreeo/djangocms-utils/)
which hasn't been updated in two years and thus is not compatible with
django-cms 3 as well.

The good thing is: django-cms introduces a paradigm shift: We are no longer
supposed to edit the placeholder fields in the admin, instead we are supposed
to create our objects in the admin and then edit the placeholder fields on the
frontend (and in fact you are now able to edit ALL your objects on the
frontend, which is totally awesome). Therefore we don't really need a fancy
M2MPlaceholderAdmin any more.

A solution for this problem can be found in my
[next post](|filename|/m2mplaceholderfield.md).

### 2. Good bye django-simple-translations

During the last two years we have built more than [70 reusable Django
apps](https://github.com/bitmazk/).  Most of them are cms plugins or cms
apphooks and when we started writing all those apps we took cmsplugin-blog as a
guideline on how to write proper django-cms apps. cmsplugin-blog was using
[django-simple-translation](https://simple-translation.readthedocs.org/en/latest/)
for i18n, so we decided that all our apps will use simple-translation as well.

Now it turns out that this was a very bad decision because django-cms 3 is
using [django-hvad](https://github.com/KristianOellegaard/django-hvad) and has
pretty awesome support for language switching on the frontend and in the
backend.

The other thing is: When you setup a project that comes with django-cms,
chances are that django-cms is the biggest and most complex app, so you can
think of it as the project's "leading" app. It only makes sense that all other
apps of that project would re-use the same dependencies that django-cms already
introduces.

Therefore: We have to say goodbye to simple-translation and migrate our models
and data to hvad. This might be difficult, but it will be worth it, because
hvad really is much better than simple-translations.

### 3. Who knows?

As I migrate all of our apps, I will probably find more hurdles and will
gradually add more detailed posts describing the solutions for each problem.

Stay tuned for the next post on how to get rid of the M2MPlaceholderField...
