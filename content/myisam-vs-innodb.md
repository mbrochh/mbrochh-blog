Date: 2012-03-18
Title: MySQL InnoDB vs. MyISAM and the foreign key constraint of death
Slug: myisam-vs-innodb.md
Category: Blog
Tags: databases, mysql, django

During the last few months I constantly ran into problems with MySQL which
drove me crazy and I finally decided to use PostgreSQL for all new projects.
Today I figured out what was going on:

On my development machine I have MySQL version 5.1.61 installed. Recent
Webfaction servers however ship with MySQL version 5.5.16. I think, the newer
version creates new tables with the much better engine InnoDB while my older
version defaults to MyISAM.

I was developing a big Django project in a highly agile way during the last
few months and my workflow looked roughly like this:

* Write tests
* Create fixtures
* Implement feature
* Rebuild database with the new fixtures
* Deploy feature at Webfaction
* Export local database
* Import local database on Webfacion server

This means for the last few months my customer and me were testing the app with
testdata only (which looked very close to the real data anyways). However, this
month the app matured enough so that I stopped importing my local database into
the Webfaction server. From now on I would create South migrations and deploy
them as usual.

Yesterday I created a new app within the project. The model of that app had a
foreign key to a model of one of the older apps. I'm sure you already know what
comes now: Because I used to import my local database into the Webfaction
server for many months, all tables had the old MyISAM engine. When I deployed
my latest feature last night and ran the South migrations everything worked
fine but when I tested the app in a browser, I got the foreign key constraint
error or death.

So I imported the server's datbase locally and asked some stupid questions in
the #mysql channel. A friendly user named ``salle`` answered within a second
and I learned about a cool SQL command which I never needed before:

    ::sql
    SHOW TABLE STATUS;

This shows, among many other informatoin, which engine each of your tables has
and at the first glance I could see that the newly created tables that came
with the South migration on the server had a different engine than all the
rest.

Another stupid question later I learned that I can convert the tables to the
other engine by simply executing:

    ::sql
    ALTER TABLE <tablename> ENGINE=<engine name>;

So I converted all MyISAM tables into InnoDB tables and all was good. I should
definitely update my local MySQL installation...
