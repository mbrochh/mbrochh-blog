Date: 2012-02-19
Title: My next approach to blogging. Again.
Slug: blogging
Category: Blog
Tags: blogging, python

I'm a netizen since 1996 or so and I think I have accounts for all major
blogging services that ever popped into existence. Yet I'm quite sure that I
have never managed to publish stuff on a regular basis or even build an
audience. This is a shame. If you know tricks to overcome this laziness, please
let me know in the comments!

I think there are two reasons for this:

# 1. I suck at writing
Writing meaningful content feels like a chore to me. One problem is that I am
not a native English speaker yet for the topics I would like to write about I
expect an English speaking audience. I guess this is just a matter of
training and self growth, so this should be a problem that can be overcome.

# 2. Technology moves too fast
In the past I have created numerous accounts at worpress.com, blogger.com,
tumblr.com. While setting up those blogs is a piece of cake, I always felt
uneasy about locking-in all this content into one service. Yes, yes, there
are probably export and import tools that should help you to get your data in
and out of all those blogging platforms but I am quite sure that migrating a
whole blog from one service to the other will result in major pain. And
let's face it. Every year or so a new hot service (like tumblr) pops up and
makes you constantly wonder if you should move on.

So I did the next obvious thing and hosted my own Wordpress instances on
Webfaction servers. While they run smoothly and fast most of the time I am
pretty sure that I would never be able to survive a slashdot effect. Besides
that, I know enough about software to not be so naive to think that you are
done when you ran the installer of Wordpress and see the initial setup. I
would fix various security issues like changing the prefix for the database
tables, the URL for the admin login, the name of the admin user and whatnot.
I would spend a day or two on optimizing my Apache settings and the .htaccess
file, even more on finding and optimizing a good theme and on installing
more than a dozen plugins. Instead of writing articles I would constantly
come back and make small improvements to the setup here and there and make
sure that everything stays up to date.

And then, just when you think that you have the perfect setup, smartphones
and tablets take over the world and you realize that you need to get a new
theme that is optimized for mobile agents and the whole trouble starts over
again.

Hosting Wordpress is just painful and definitely not fun. When you do
something in your spare time it should always be fun.

# What I want

* I want to be able to write my articles in Vim
* I want to write my posts in Markdown.
* I want to be able to put my articles under version control.
* I don't want to think about hosting and scaling.

A few weeks ago I discovered two services, [calepin.co](http://www.calepin.co)
and [scriptogr.am](http://www.scriptogr.am) which looked very promising and
very close to my needs. Unfortunately the creator of calepin.co has some
strange opinions about the future of publishing and therefore keeps the service
way too minimalistic. While scriptogr.am looks like a very decent service, the
only problem here is that you have to host your stuff on Dropbox. While this
somehow meets my requirements of version control, I would prefer _real_ version
control on Github.

Thankfully out of a sudden [Daniel
Greenfeld](https://twitter.com/#!/pydanny/status/171102804574875648) posted
about his Pelican powered blog on Github. Luckily he included a first blog post
which describes how to setup a similar blog with just four simple lines of
code.

I was hooked. So I set up this blog in an hour or so. Let's see if I can
finally meet my goal to publish meaningful content on a regular basis :)
