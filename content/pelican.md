Date: 2012-02-20
Title: Blogging with Pelican and GitHub
Slug: pelican
Category: Blog
Tags: blogging, python

While it took me indeed just four lines of code and thirty minutes to setup the
first version of this blog, I couldn't resist to geek over it for a few more
hours and create a nice and clean approach to publishing this blog with
[Fabric](https://github.com/fabric/fabric),
[Pelican](https://github.com/ametaireau/pelican) and
[GitHub](http://github.com).

# What to expect

When you follow these instructions, you can expect the following:

* A simple static blog website with a simple yet beautiful theme.
* Possibility to change any aspect of the site as you wish.
* Writing your blog posts in the editor of your choice with
  [Markdown](http://daringfireball.net/projects/markdown/).
* All your content is under version control on GitHub. This means that people
  can send you pull requests and suggest improvements to your posts, which is
  just awesome.
* Publishing your posts by simply calling `fab publish:'Commit message'`.
* Free hosting on GitHub. I guess you don't need to worry to make it to the
  front page of [Hacker News](http://news.ycombinator.com/).

I should mention that Pelican is a Python project and therefore it wouldn't
hurt if you knew a bit about Python. I will assume basic Python knowledge here.
Let's get started:


# Activate GitHub Pages

Just create a new repository called `username.github.com`. Whatever you place
in here will be served at `http://username.github.com`. For more information
please see the [GitHub Pages Documentation](http://pages.github.com/).


# Setup your repository

First create a folder on your disk for the new project:

    ::sh
    mkdir $HOME/Projects/myblog
    cd $HOME/Projects/myblog

Next setup your `source` folder. This is the folder where you will write your
articles and call pelican to generate your static html output:

    ::sh
    mkdir source
    cd source

    # We will steal some files from my own repo here:
    wget https://github.com/mbrochh/mbrochh.github.com/raw/master/source/requirements.txt
    wget https://github.com/mbrochh/mbrochh.github.com/raw/master/source/fabfile.py
    wget https://github.com/mbrochh/mbrochh.github.com/raw/master/source/settings.py.sample settings.py

The sample `settings.py` you just got from my own repo will need some changes
now. Have a look at it and edit it so that it fits your needs.


# Setup your virtualenv

If you have never used virtualenv and virtualenvwrapper before, now is the
time to learn about it. Usually this is what you need to do to install it:

    ::sh
    sudo easy_install pip
    sudo pip install virtualenv
    sudo pip install virtualenvwrapper
    export WORKON_HOME=~/Envs
    source /usr/local/bin/virtualenvwrapper.sh
    # also add export WORKON_HOME=~/Envs to your .bashrc file

We will use virtualenv to install fabric and pelican:

    ::sh
    mkvirtualenv -p python2.7 blog
    workon blog
    pip install -r requirements.txt


# Create your first post

Now is the time to create your first post:

    ::sh
    # make sure to be in the source/ folder
    mkdir -p posts/2012/02/  # insert appropriate year and month here
    cd posts/2012/02/
    touch hello-world.md
    nano hello-world.md

To learn more about how to write your articles with Markdown or
reStructuredText for Pelican, have a look at
[writing articles using pelican](http://pelican.notmyidea.org/en/latest/getting_started.html#writing-articles-using-pelican).

Your article should look similar to this:

    ::text
    Date: 2012-02-20
    Title: Hello world
    Category: Blog
    Tags: blogging, test

    Lorem ipsum

I like to create meaningful commit messages for the edits of my `.md` files and
separate them from the changes that the Pelican output generates, therefore now
it is a good time to create a commit:

    ::sh
    git add .
    git commit -am "Created my first post."


# Publish your first post

This is the interesting part! You will use Pelican now to generate the output
for your blog:

    ::sh
    # make sure to be in the source/ folder
    pelican . -o ../ -s settings.py
    git status

When you run `git status` you will see that Pelican generated a whole bunch
of files in your root directory. Open your `index.html` and have a look at
your new blog.

If you see that something went wrong, you might want to destroy the generated
output:

    ::sh
    # make sure to be in the root folder and be sure that your .md file changes
    # have been committed
    git clean -df

Now you can edit your `.md` files again and generate the output again. If you
are happy with your output, it is time to publish it:

    ::sh
    # make sure to be in the root folder
    git add .
    git commit -am "Pelican output"
    git push origin master


# Publishing with fabric

As you have seen, the workflow of editing your posts is always the same. First
you edit your `.md` files, next you commit your changes and give a meaningful
commit message and at last you generate the output and commit it with a
standard commit message. Finally you push to Github which will make your
changes visible.

To make this workflow easier, I have created a little Fabric script. Now you
can just edit your `.md` files and once you are done, call Fabric:

    ::sh
    fab publish:'My commit message'


# Setting up a custom domain

As if all this isn't awesome enough, GitHub makes it really easy to create
custom domains for your GitHub page. All you need is to place a file called
`CNAME` in the root of your project and add the following content:

    ::text
    yourdomain.com

Then point the A record of your domain to the IP address of GitHub. For more
information have a look at the instructions about
[custom domains on GitHub](http://pages.github.com/#custom_domains).


# How to embed images?

If you need to embed images, you can just add them to the folder
`source/images/` and link to them in your `.md` files like so:
`![Alt text](./static/images/yourimage.png)`.


# Thanks!
That's it. I hope I didn't forget anything. I would like to thank
[Alexis Metaireau](https://twitter.com/ametaireau) for the great work on
Pelican. There is a small and friendly group sitting at #pelican on Freenode
and while I was writing this post, I submitted a pull request to Pelican which
got merged almost immediately. The project is really worth a closer look!
