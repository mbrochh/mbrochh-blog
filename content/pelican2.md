Date: 2013-05-15
Title: Pelican and Github Pages
Tagline: Blogging on The Shoulders of Pelican, Markdown & Github Pages
Slug: pelican2
Category: Blog
Tags: blogging, python

One year ago I blogged about [Pelican](|filename|/pelican.md) and up until
today this remains the most frequented post in my blog. However, in the
meantime Pelican got two major version bumps and is much more powerful now (and 
easier to use). So let's see how to setup your blog with Pelican and host it
on Github Pages today...

### Create a virtualenv

As usual, before you do anything with Python, create a virtual environment for
your Project.

    #!sh
    mkvirtualenv -p python2.7 blogging
    pip install Pelican==3.2
    deactivate
    workon blogging

### Quickstart Pelican

Pelican now comes with a [quickstart](https://pelican.readthedocs.org/en/3.2/getting_started.html#kickstart-your-site)
command similar to Sphinx which will setup the recommended folder structure for
you. When running the command, I think I answered all questions with their
default answers.

    #!sh
    mkdir -p ~/blogging/src
    cd ~/blogging/src
    pelican-quickstart

At this point you will have a nice project structure and you should initiate a
Git repository and a `.gitignore` file:

    #!sh
    git init
    nano .gitignore

    # Content of the .gitignore file:
    *.pid
    *.pyc
    *.swp
    output/

### Add some content

`cd` into the `content` folder and create your [markdown content](https://pelican.readthedocs.org/en/3.2/getting_started.html#writing-content-using-pelican)
files there. While you are writing your post, you will likely want to see your
latest changes in a browser. For this reason pelican now provides a simple
development server which you can start like so:

    #!sh
    make devserver

Please note that when you quit that command with `CTRL+C`, the server is still
somehow running in the background. In order to really quit it, you need to run:

    #!
    ./develop_server.sh stop

This will also be necessary if you saved a file with incorrect syntax and
caused an error in the devserver. The server output will usually describe
nicely what the error was but it will not restart properly once you corrected
the error, so you need to do that manually.

### Hosting on Github Pages

[Github Pages](http://pages.github.com/) is a fantastic way to host static
websites in Github's cloud. In my old post I described how to do this using
*User pages* but I would no longer recommend this because it expects you to
have the output in your project root, which we don't have any longer. Our
output is in the `output` directory and it is good that way because we can now
delete that directory prior to each publish.

Instead we will use *Project Pages*. Simply create a new project on Github,
make your initial commit in your pelican project and push it into your new
Github project.

When using a *Project Page* you need to put your HTML output into a branch
called `gh-pages`. I have never really understood how to create and maintain
this branch, but thankfully there is an awesome script called
[ghp-import](https://github.com/davisp/ghp-import) which will do all the magic
for you. Simply install that script into your virtualenv:

    #!sh
    workon blogging
    pip install -e git+git://github.com/davisp/ghp-import.git#egg=ghp-import
    deactivate
    workon blogging

Now you can publish your blog for the first time using one of Pelican's Make
commands:

    #!sh
    make github

Whoa. That was easy!

### Use your own domain

If you would like to show your blog under your own domain, just set your
domain's A-Record to `204.232.175.78`. Now we need to make sure that there is
a file called `CNAME` in the output directory. In order to achieve this, `cd`
into your `content` directory and create a folder `extra` and put that file
into that folder:

    #!sh
    cd ~/blogging/src/content/
    mkdir extra && cd extra
    nano CNAME

    # Put your domain name into that file, i.e.:
    example.com

Now add the folowing setting to your `pelicanconf.py`:

    #!sh
    nano pelicanconf.py
    FILES_TO_COPY = (
        ('extra/CNAME', 'CNAME'),
    )

This makes sure that the `CNAME` file will be copied from the content folder
into the output folder on each publish. Don't forget to wait a few hours for
the CNAME changes to propagate.

### Themes & Settings

If you want another theme, you should check out [pelica-themes](https://github.com/getpelican/pelican-themes).
Just clone that repository and change your theme setting in `pelicanconf.py`:

    #!sh
    git clone git://github.com/getpelican/pelican-themes.git ~/pelican-themes
    cd ~/pelican-themes
    git submodule init
    git submodule update

    nano ~/blogging/src/pelicanconf.py
    # Change the THEME setting:
    THEME = '/Users/martin/pelican-themes/basic'
