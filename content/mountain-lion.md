Date: 2012-07-26
Title: Fixing OSX 10.8 after Mountain Lion upgrade
Slug: mountain-lion
Category: Blog
Tags: apple, osx

Out of habit I opened the AppStore on my MacBook Pro yesterday and found a big
fat new app in the spotlight: OSX 10.8 Mountain Lion. I paid my 15 bucks,
downloaded the 4GB over night and started the installation this morning. It
estimated 34 minutes to install but I don't know if that is true because I went
back to sleep.

When I got up, the Mountain Lion login screen greeted me. If this is not an
awesome upgrade experience, I don't know what is. 15 EUR and three clicks,
other than that totally unattended update. I cannot see any way how Microsoft
and Windows will survive the next decade.

I guess from a user point of view this is the best experience possible. For us
developers it doesn't look that good, but that is to be expected and the same
happens on Ubuntu as well, so I won't complain here.

Here is what I had to do to get my Python projects back up and running:

## Re-Install Command Line Tools

With the Mountain Lion upgrade I also upgraded a few other apps, such as XCode.
Unfortunately it seems that the Command Line Tools I had installed are no
longer working, so the natural thing to do is, login to the Apple Developer
site and download the latest version. Turns out that version is not compatible
with OSX 10.8. **What the fuck?**

Some googling revealed that you can install these tools now via XCode by going
to ``Preferences --> Downloads``. I clicked at the ``Install`` button next to
``Command Line Tools`` and had to enter my Apple Developer ID and password.
After a few seconds XCode tells me that I don't have access to that download
and that I should contact Apple to resolve access problems. Turns out this is
a bug in XCode that has been fixed for some but not for others. I'm seem to be
one of the others. **What the fuck?**

Some more googling revealed that you can download a special, older version
of the Command Line Tools and install it from the ``.dmg`` file. This works
although that version's description is exactly the same, I don't see why the
latest version does not work. **What the fuck?**

Anyways, the link is here: [cltools_mountainliondp2_march12.dmg](http://adcdownload.apple.com/ios/ios_simulator__resigned/cltools_mountainliondp2_march12.dmg)

## Re-Install Parallels

I should have started Parallels before upgrading to Mountain Lion, then it
would have upgraded itself. Instead after logging in to Mountain Lion it
told me that it found incompatible software which it moved to some graveyard
folder. No more Parallels for me. Thankfully I could login at the Parallels
website and retrieve a download link for the latest version [here](http://www.parallels.com/download/build/desktop/)

## Update zsh

Something in my zsh seemed to be broken because whenever I tried to use TAB
for folder completion I got this error:

    (eval):setopt:3: no such option: NO_ignoreclosebraces

Updating zsh can only be done if you went through the various what-the-fucks of
updating your Command Line Tools first, after that it simply is:

    brew update
    brew uninstall zsh
    brew install zsh

And fixed my problem right away.

## Re-Install Python

I actually did this at the end of my journey because it turned out that even
though I updated virtualenv and virtualenvwrapper I was not able to install
anything into my virtualenvs because pip always tried to install it into
``/Library/Python/2.7/site-packages/`` which of course resulted in ``Permission
denied`` errors. ``brew list`` showed that I actually installed Python via
homebrew for some reason (I assume because of pygame), so I thought it might
be a good idea to re-install Python:

    brew uninstall python
    brew install python --framework

After this I ran into several other problems. I'm not sure if this is really
necessary but setting up my ``PATH`` like this seemed to help:

    export PATH=/usr/local/bin:/usr/local/sbin:/usr/local/share/python:$PATH
    # Include user's bin folder.
    if [ -d "$HOME/bin" ] ; then
        export PATH="$HOME/bin:$PATH"
    fi

## Re-Install Python stuff

It turned out that I could no longer activate my virtualenvs. Here is what I
had to do:

    sudo easy_install pip
    sudo easy_install mercurial
    sudo pip install virtualenv
    sduo pip install virtualenvwrapper
    sudo touch /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/distutils/__init__.py

The last one is wonderful. Somehow Apple ships the Python stuff as compiled
``.pyc`` files without the ``.py`` files. I can't remember if it was when I
tried to use ``pip install`` or ``workon`` but I got that error telling me
that ``/distutils/__init__.py`` cannot be found. Google told me that I can
just create that missing ``.py`` file. **What the fuck?**

I also re-installed some packages that I like to install globally instead of
installing them into each and every virtualenv:

    sudo pip install psycopg2
    sudo pip install mysql-python
    sudo pip install PIL

## Re-Install Java

When I tried to start solr a pop-up offered to download the latest Java version.

## Set iTerm to xterm-256color

You might have a problem when running Vim inside of GNU Screen or tmux. It
might no longer show the correct color theme. This is because iTerm forgot it's
setting for ``Report Terminal Type``, which you can set at ``Preferences -->
Profiles --> Default``. Set it back to ``xterm-256color``.

## That's it

This whole thing took me exactly 4 hours including the writing of this blog
post. It also took so long because I had to reinstall a huge virtualenv over
and over again until it finally worked without errors. Not too bad actually and
I found it quite amazing that MySQL and Postgres still worked.
