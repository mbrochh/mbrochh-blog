Date: 2012-06-??
Title: Creating a game with Pyglet
Slug: slug
Category: Blog
Tags: python, pycon, conferences
status: draft

# Installation

As always, it doesn't work out of the box on OSX without some extra steps:

    ::sh
    # Source: https://twistedpairdevelopment.wordpress.com/2012/02/21/installing-pyglet-in-mac-os-x/
    mkvirtualenv -p python2.7
    pip install hg+http://pyglet.googlecode.com/hg/
    easy_install pyobjc==2.2

# First steps

I am following this tutorial: http://steveasleep.com/pyglettutorial

* I don't like the structure he suggests. Why ``version1/`` folder? I have git
  for versioning stuff.
