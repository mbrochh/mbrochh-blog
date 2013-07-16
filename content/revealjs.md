Date: 2013-07-02
Title: Reveal.js and Github Pages
Tagline: How to Host Your Slides on Github With Reveal.js, Jinja & Fabric
Slug: revealjs
Category: Blog
Tags: python, presentations, howto

Yesterday, I described why [my current presentation stack needs an overhaul](http://martinbrochhaus.com/presentations.html).
Today I'm going to show you my new stack. This how-to will introduce a little
helper project that will allow you to easily kickstart a new Reveal.js
presentation, split it up into subfiles and host it on Github Pages.


### Motivation

When I played around with [Reveal.js](http://lab.hakim.se/reveal-js) I
immediately fell in love with it.  There is just one thing that bothers me: You
are supposed to put your whole presentation into one big `index.html` file. I
don't want to do this because I'm going to collaborate on the slides with
others and I want to avoid merge conflicts. Therefore I would like to split
that one big file into many small ones (i.e. one file per slide).

I also want to host the slides on Github Pages (just like this blog).
Unfortunately Github Pages is really just pure static HTML, therefore I can't
do server side includes or use PHP to include other .html files. I wasted an
hour trying to include .html files with JavaScript but I ran into cross-origin
resource issues and when I finally got it working, the styles of the slides
were all messed up.

So clearly, we need a templating engine which is able to include other sub
templates in its main template file. [Jinja](http://jinja.pocoo.org/) can do
that and if you are familiar with Django's templating engine you will feel at
home with Jinja immediately.

Ultimately, this little "hack" is another great example why Python and its
ecosystem are awesome and why everyone should know a little bit of Python.
Remember: We are not trying to do any coding here. We just want to produce
some beautiful (and powerful) presentation slides.

So let's start cooking:


### Bootstrap Reveal.js

For your convenience I have prepared a little template-project on Github to
[kickstart your Reveal.js presentation](https://github.com/mbrochh/reveal-template).
All you need to do is clone the project and initiate a new repository:

    git clone https://github.com/mbrochh/reveal-template your_presentation_name
    cd your_presentation_name
    rm -rf .git
    git init
    git add .
    git commit -am "Initial commit"

You should be able to execute `open presentation/index.html` and see a basic
presentation with a few test slides.


### Install requirements

In order to use Jinja and Fabric you need to install a few Python packages.
As always, you should first create a virtual environment and then install the
packages into that environment:

    mkvirtualenv -p python2.7 your_presentation_name
    pip install -r requirements.txt

This will take a while. When it's done you should be able to run `fab build`.

You might also want to install [observr](https://github.com/kevinburke/observr)
in order to build your presentation whenever you save one of the template
files.


### Structure with Jinja

As always, when you want to publish stuff on Github pages, you need to have
one source folder with your raw content, which will be part of your Git
repository and one destination folder with your compiled content which will
usually not be part of the Git repository.

In our case the source folder is called `source` and the destination folder
is called `presentation`. I cheated a little bit. Not everything in the
destination folder is under `.gitignore`. I put the Reveal.js sources in there.
A cleaner solution would have been to add those sources as a git submodule
and copy them into the presentation folder every time you run `fab build`.
Maybe I will do that later. However, the index.html file in the
presentation folder is in .gitignore and will be compiled every time you run
`fab build`.

Now have a look at the `source` folder. You will find six files:

    - source/
      - base.html
      - index.html
      - title.html
      - test_markdown.html
      - test_code.html
      - test_backgrounds.html

`base.html` contains all the HTML boilerplate stuff that is needed to display a
proper Reveal.js presentation. Once you have set this up (i.e. included all CSS
styles and plugins, changed the title etc.) this will rarely ever change again.

`index.html` is our Jinja template. It *extends* `base.html` and *includes*
all the remaining files, which are our individual slides.


### Build with Fabric

In order to create the final `presentation/index.html` we need to tell Jinja to 
take the `source/index.html` template and render it into the destination
folder. I have created a tiny Fabric task for this, so all you need to do is
to run:

    fab build


### Continuous building with Observr

Now when you are working on your slides you probably want to review them in
the browser all the time, so you would have to run `fab build` all the time,
which sucks. A proper solution would be to setup a tiny webserver which listens
to requests and returns the rendered template (might do that later) but for
once I suggest that you simply install [observr](https://github.com/kevinburke/observr) and keep it running in a
separate terminal widow. In order to watch for changes, I have created a small
shell script which you can execute via

    ./source-watcher.sh

**Hint**: Don't forget to stop observr when you don't need it any more. It eats
20% CPU all the time, which will eat your battery in no time when you are on
the go ;)


### Publish on Github Pages

In the `requirements.txt` file I have added the awesome [ghp-import](https://github.com/davisp/ghp-import)
tool which really opened up the glorious world of Github Pages for me. Again I
provided a small Fabric task, so in order to publish your presentation simply
run

    fab publish

It will create the `gh-pages` branch and push it. A few seconds later you
should be able to see your presentation at
`http://username.github.io/your_repo_name`.


### Control via Socket.IO

I haven't had the time to try this myself, yet, but the instructions for
[multiplexing](https://github.com/hakimel/reveal.js#multiplexing) in the
Reveal.js README seem to be straightforward. The idea is that you start a local
webserver and your audience will browse to your IP. Now your audience will be
connected to you in real-time, so when you change a slide, it will change on all
screens.

That's it! I hope my little [reveal-template](https://github.com/mbrochh/reveal-template)
will be useful to someone and allow you to publish awesome presentations in no
time - have fun!
