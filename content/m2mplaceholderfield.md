Date: 2013-10-27
Title: Getting Rid of M2MPlaceholderFields
Tagline: Because You Can't Use Them With django-cms 3 Any More
Slug: m2mplaceholderfields
Category: Blog
Tags: python, django, django-cms, howto
status: draft

In my last post I gave an overview over the two major hurdles I had to overcome
in order to migrate
[django-multilingual-news](https://github.com/bitmazk/django-multilingual-news).
to django-cms 3.

In this post I will describe how I took the first one:

## Migrating away from M2MPlaceholderField and M2MPlaceholderAdmin

We can't use the M2MPLaceholderAdmin any more because it uses a widget that
no longer exists in django-cms 3.

The idea for a proper migration is as follows:

1. On the model that has the M2MPlaceholderField, we add new PlaceholderFields
2. After that we add a datamigration which creates new Placholders for these
   new fields and moves all the plugins from the old placeholders to the new
   ones.
3. Finally we can remove the old M2MPlaceholder field.

This sounds trivial at first, but in fact it took me quite a while to figure
out because there is a lot of magic involved in the PlaceholderFields that will
not be reflected inside the South datamigration.
