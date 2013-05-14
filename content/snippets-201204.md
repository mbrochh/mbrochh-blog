Date: 2012-04-21
Title: Snippets of April 2012
Slug: snippets-201204
Category: Blog
Tags: snippets, ubuntu, screen, ssh, mercurial, self growth

This is my second post in a series of (almost) monthly posts about small bits
and pieces of wisdom that amazed me. You can find the first post here:
[Snippets of February 2012](http://martinbrochhaus.com/2012/02/snippets-201202.html)


# Ubuntu: Static Application Switcher

App switiching with ALT+TAB became a major pain since Ubuntu introduced that
horrible Unity interface. The simple solution is to open CompizConfig Settings
Manager and enable "Static Application Switcher" under "Window Management".

I think it is much much more intuitive and effective to have a static list of
windows instead of an endlessly rotating one.

# Scrolling and Copy & Paste in GNU Screen

I really got to love screen during the past 4 months and usually work in a
session with 7 windows open. The problem is, when I swtich to window 1 to see
the output of my tests and there is a huge traceback, I cannot use my terminal
to scroll up because I will scroll into whatever I saw in the windows before
(probably Vim).

The trick is to use Screen's scroll mode by pressing ``CTRL+A ESC``. It will
display a message saying that copy mode is activated and now you can move the
cursor with the usual Vim keybindings. Pressing ``SPACE`` or ``ENTER`` once
sets a marker and pressing it again will copy everything between the first and
second marker into the clipboard.

You can paste the clipboard via ``CTRL+A ]``. Yea, I know. Read the fucking
manual... :)

# SSH Keep Alive

Whenever I need to SSH into my various servers I get connection timeouts all
the time. Somehow most people don't suffer from this so this seems to be a
problem with my Ubuntu installation, but recently I found a solution that works
for me:

On my servers, I now set this:

    ::text
    # in ~/.ssh/config:
    ServerAliveInterval 60

    # in ~/.screenrc
    caption always '%c:%s'

Now I just need to remember to start a screen session right after I login. The
screen setting will render a clock at the bottom of the screen which is enough
to have a steady bit of traffic going through SSH for not kicking me out of the
server any more.

# Nerdy IT Jargon

I can't remember where I learned about these but I love them:

* ``<=>`` is called the spaceship operator
* Writing variable names ``LikeThis`` is called CamelCase. I knew this for
  years, but:
* Writing variable names ``like_this`` is called ``snake_case``. Very Pythonic,
  isn't it?

# HG Facepalm

I can't believe that this actually happened, but if you have something from
Bitbucket in your requirements.txt and try to pip install it, you might get
a weird error saying that the pip call to Bitbucket returned code 1 and this
pip stops installing.

This is because a recent version of Mercurial returns 1 if ``hg pull`` doesn't
return any new changes (which happens most of the time).

However, pip (and almost every other software on this planet) thinks that a
return value of 1 means a failure and just stops.

Thankfully Mercurial fixed this quickly and reverted that change, so if you are
suffering from the "bad" version, you might want to upgrade your Mercurial
installation.

* [Mercurial upgrade notes](http://mercurial.selenic.com/wiki/UpgradeNotes)
* [Relevant GitHub issue for pip](https://github.com/pypa/pip/issues/454)

# Great blog posts

I currently have 190 subsriptions in Google Reader and I am following 298
awesome people on Twitter. These lists are carefully curated by myself and I
usually enjoy reading almost everything that comes in through those streams.
Here are some posts that, to me, should be spread as far as possible.

* [9 Essential Skills Kids Should Learn](http://www.dailygood.org/view.php?sid=194)
  The longer I work on my own company Bitmazk Pte. Ltd. the more I realize that
  (at least in the IT business) traditional education is completely worthless.
  I have the feeling that I will put in quite some effort to educate my own
  kids in a very different way than I was educated myself. This post gives some
  very very nice ideas.

* [The Only Guide to Happiness You’ll Ever Need](http://www.stumbleupon.com/su/9IbGnD/zenhabits.net/the-only-guide-to-happiness-youll-ever-need/)
  The title says it all. After reading "Mindfulness in Plain English" several
  times, the pursuit of hapiness has become a very important part of my life
  that I try to consciously improve day after day. I've surely not mastered
  this aspect of my life but I can tell that this list nails it.

* [Do things, tell people](http://carl.flax.ie/dothingstellpeople.html)
  This. Absolutely true. Whenever I did something in the open, no matter how
  small, lame or unimportant, an incredible chain of events unfolded itself
  in front of me that enriched my life in ways that I can't put into words.
  Please! If you have a little bit of energy left at the end of your day, get
  your ass up, do things, and tell people!

* [Good Agile, Bad Agile](http://steve-yegge.blogspot.com/2006/09/good-agile-bad-agile_27.html)
  It sad but true: This whole Scrumm and Agile movement is a big scam. This
  rant explains why. Thought provoking read.
