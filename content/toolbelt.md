Date: 2013-05-16
Title: OSX Django Toolbelt
Tagline: Everything You Need to Build Django Apps on OSX
Slug: toolbelt
Category: Blog
Tags: osx, django 

Every time I mentor someone about web development with Django, we spend 
countless hours setting up his or her development machine. I'm getting sick of
it, so I thought I might write it all down.

This post will help you to setup a fresh MacBook in such a way that enables you
to start building complex Django sites. It will take a very long time, probably
between six to ten hours and it will be frustrating because I didn't test
everything presented here (I don't have a clean machine at hand). 

Take that as part of the fun. After all, web development (or software 
development in general) is just that: It is frustrating. Things never work like
they should but you will be amazed how accurately Google will solve your
problems when you read all those error messages and search for them.

Let's get started...

### Get Yourself a Butler

Before you do anything with your Mac, do yourself a favor and install [Alfred](https://itunes.apple.com/de/app/alfred/id405843582?l=en&mt=12)
from the AppStore. It allows you to press `OPTION+SPACE` and type whatever you
want to start. It's awesome. I never have icons on my desktop and I never use
the icon bar at the bottom. What is it even called? Really. Trust me. Nothing
beats Alfred. 

> Hint: You can even use Alfred as a quick calculator or start
> Google / Wikipedia / Amazon searches from it.

### Install XCode & Command Line Tools

When you get your new MacBook, it is just an expensive toy. The first thing you 
need to do is to go to the AppStore and install XCode. This will take a very 
long time. Afterwards you need to start XCode and agree to the terms and 
conditions. Finally you need to install the Command Line Tools in order to be
able to compile the many other tools you will install later.

In order to install Command Line Tools, open XCode, go to 

    #!sh
    Preferences --> Downloads --> Components

and click the *Install* button next to *Command Line Tools*. This will also
take quite some time and might require a reboot.

Congratulations! Now you have taken the first big step to turn your expensive
toy into a life companion that will allow you to build things and change the
world. ;)

### Install Database Stuff

#### Postgres.app

While XCode is downloading, you can use your time and install a few more tools.
First of all you should install [Postgres.app](http://postgresapp.com/).

> **IMPORTANT**: After downloading the app, DO NOT EXECUTE IT! Move it into the
> *Applications* first, then execute it for the first time. 

You might want to add the app to your startup applications. If not, remember to 
restart it after a reboot.

#### pgadmin3

Now that you have postgres installed, you should install [pgadmin3](http://pgadmin.org/download/macosx.php).
Once installed, start it and click at

    #!sh
    File --> Add Server

Fill it out like so:

    #!sh
    Name: Any name (i.e. localhost)
    Host: localhost
    Port: 5432
    Username: username 

Username is the important thing here. *Postgres.app* does not install a
postgres user, like the usual installation would do. Instead it uses your admin
user account to manage the database. So you should fill in your OSX username
here. Press OK and double click your newly created server. If all went well,
you should see *Databases*, *Tablespaces*, *Group Roles* and *Login
Roles*.

### Pimp Your Terminal

#### iTerm2

First of all, install [iTerm2](http://www.iterm2.com/). This will save you some
trouble with copy and paste issues and color schemes and it has proper 
implementation of the fullscreen mode (which I use all the time) and has other
neat things like notification and beeps when something has changed in one of
your many open tabs.

By the way: I like to use the [Solarized Dark Theme](https://code.google.com/p/iterm2/wiki/ColorGallery)
for my terminal.

#### Install Homebrew

From here onwards we will need to install a ton of tools via homebrew, so
simply install it like so: 

    #!sh
    ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"

Don't forget to run `brew doctor` and `brew update`, when you are done. It will
probably find some problems. For example you might have to add some folders to
your `$PATH` environment variable. You might want to put this into your
`~/.bash_profile`

    #!sh
    export PATH=$HOME/bin:/usr/local/bin:/usr/local/sbin:/usr/local/share/python:$PATH

Don't forget to create your own `~/bin` folder. Finally install wget already,
because we will need it in the next step:

    #!sh
    brew install wget

#### zsh

If you are developing software, you will probably use the terminal all the time.
You should make it an awesome place to be. Thanks to homebrew, installation is
really simple:

    #!sh
    wget --no-check-certificate https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh

It will make zsh your default shell, so after installation, quit the 
terminal and start a new one and you should see a slightly different command 
prompt.

zsh can do a million things, I don't even know one percent of them but here is
what you will use all the time:

**autojump** learns which folders you use often. If you are always cd-ing
around in a folder called `~/Projects/django/myapp`, you can now simply type 
`j my` and autojump will magically cd into that folder.

**Tab completion** even works when you type any part of filenames, not just the
beginning. So if you know that there is a file `foo_bar_95.txt`, just type
`bar` and press `TAB` and be amazed. Have many files or folders with similar
names? Just hit `TAB` multiple times and jump between the items, press
`SHIFT+TAB` to jump back.

**Command history** can be called pressing the arrow up key. We all know that.
And we all have been in that situation where we have to hit arrow-up 30 times
in order to get back to that old long command we typed 20 minutes ago. Ugh.
With zsh you can type the beginning of the command (let's say the first letter)
and press arrow-up and you will only get the part of the history of commands
that started with that letter. VERY useful.

The **Command prompt** is also supercharged with plugins. For example, if you
cd into a git repository, the command prompt will change and show you the
branch you are on and if you are behind of any upstream changes.

What am I rambling so much? Go and install it already, for gods sake!

#### Useful Command Line Tools

Since we have an awesome terminal and shell now, we should install some tools.
First of all

    #!sh

    # Good for sending HTTP requests to APIs
    brew install curl

    # Screen multiplexer, extremely useful when working with many tabs
    brew install tmux
    brew install reattach-to-user-namespace

    # This fixes a problem with the virtualenvwrapper plugin of oh-my-zsh
    brew install coreutils
    mkdir -p ~/bin && cd ~/bin && ln -s `which greadlink` readlink

    # This allows for awesome bash completion for all kinds of things, such as
    # fabric files.
    brew install bash-completion
    cd /usr/local/etc/bash_completion.d
    wget https://github.com/marcelor/fabric-bash-autocompletion/raw/master/fab


#### One word about tmux

Use it! Really, don't be scared. There are many good
tutorials out there. When you are doing web development, you will always have
at least 3 terminal windows open: One to start your Django development server,
one to cd around in your folders and create files and one to actually write 
code. Maybe you will have another one for compiling your LESS or SASS files 
into CSS and another one to automatically execute your test suite on each file
save. Now imagine you are working on three different projects simultaneously.
That would be up to 18 tabs in your terminal. What if your terminal crashes?
You would lose all tabs and be a very sad developer. As long as you don't 
reboot your machine, tmux will keep running, even when you close your terminal.

There is another very similar tool called screen. I like tmux more because of
it's awesome possibility to do [pair programming](|filename|pair.md), but I 
still often use screen when I ssh into my servers. To make life easier, I have
created a [.tmux.conf](https://github.com/mbrochh/mbrochh-dotfiles/blob/master/.tmux.conf)
where I re-mapped all keys to match the key bindings in screen so that I can
switch between both tools without needing to think.

Here are a few commands that will get you up and running quickly:

    #!sh
    # Start the tmux server and attach to your first session
    tmux 

    # Create a new window
    CTRL+a c

    # List all windows that you have so far. Navigate between them with j and k
    CTRL+a w

    # Quickly switch between the last two windows
    CTRL+a a

    # Close a window. When you close the last one, the session ends
    exit (or CTRL+d)

    # You should  still have one window open, close your terminal, open a new
    # one and see if the session is still there
    tmux ls

    # Re-attach to your old session
    tmux a -t <session id>

That's pretty much all I know and ever need. There are some advanced use cases
when you need to scroll up in a tmux window and copy and paste code, but with
iTerm2 scrolling should work just fine with your touch-pad or mouse wheel.

### Install node.js

Sooner or later you will use Twitter Bootstrap as a CSS framework (or any other
CSS framework) and you will fall in love with [LESS](http://lesscss.org/) or
[SASS](http://sass-lang.com/) and apparently the best way to compile less files
into css files is to use the less package of node.js:

    #!sh
    brew install nodejs
    curl http://npmjs.org/install.sh | sh
    npm install recess uglify-js jshint -g
    npm install less --global

You will have to restart your terminal in order to use the `lessc` command. The
usage is simply:

    lessc some-file.less some-file.css

It will compile the .less file into a .css file.

### Finally some Python stuff

Whenever you do anything with Python, always create a virtual environment for
it. This will enable you to work on two different projects at the same time. 
One might use Django 1.4.5 while the other one uses Django 1.5.1. Since you are
using virtual environments for both projects, you can install both Django 
versions on your machine without ever running into version conflicts.
Let's install the necessary tools:

    #! sh
    # use easy_install to install pip
    # then never use easy_install again
    # it's like using Internet Explorer to install Firefox
    # or like using Firefox to install Chrome
    sudo easy_install pip

	# install virtualenv
	sudo pip install virtualenv
	sudo pip install virtualenvwrapper
	export WORKON_HOME=~/Envs
	source /usr/local/bin/virtualenvwrapper.sh

    # put the following into your ~/.bash_profile and ~/.zshrc
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
    export WORKON_HOME=$HOME/Envs
    export PIP_VIRTUALENV_BASE=$WORKON_HOME
    export PIP_RESPECT_VIRTUALENV=true
	source /usr/local/bin/virtualenvwrapper.sh

Try to create your first virtualenv:

    mkvirtualenv -p python2.7 test

It should create the virtual environment at `~/Envs/test` and you can 
deactivate it by typing `deactivate` and activate it by typing `workon test`.

Now always remember, when you work on your `test` project, always activate it's
virtualenv. When the virtualenv is active, you can use `pip install Django` and
it will not be installed into your global package space but into the virtualenv
(into `~/Envs/test/lib/python2.7/site-packages/django`).

### Install VIM

The last step before you can start changing the world by creating the next 
Facebook is to install a good IDE. 

The short version is this:

    #!sh
    sudo easy_install mercurial
    mkdir ~/opt
    mkdir ~/src && cd src
    hg clone https://vim.googlecode.com/hg/ vim
    cd vim/src
    ./configure --enable-pythoninterp --with-features=huge --prefix=$HOME/opt/vim
    make && make install
    mkdir -p $HOME/bin
    cd $HOME/bin
    ln -s $HOME/opt/vim/bin/vim

This will download and compile vim with the Python interpreter enabled. You 
will place a symlink to the new vim executable in your `~/bin` folder to make
sure that the command `vim` will actually start your own compiled version 
instead of the version that comes with the OS.

Now you have to install a number of plugins and setup your .vimrc file 
properly. Check out my PyCon talk about [Vim As a Python IDE](https://www.youtube.com/watch?v=YhqsjUUHj6g)
to learn more. Please note that I don't use the python-mode plugin any more,
instead I am using [jedi-vim](https://github.com/davidhalter/jedi-vim).

If you are new to vim, start learning by simply typing `vimtutor`. The tutorial
should take you about an hour and is well worth your time. In the beginning
you will want to have a look at the [vim cheatsheet](http://www.viemu.com/a_vi_vim_graphical_cheat_sheet_tutorial.html)
every now and then.

I should probably write a post about how to setup vim, soon...
