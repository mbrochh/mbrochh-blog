Date: 2013-01-17
Title: How to manage Twitter Bootstrap
Slug: bootstrap
Category: Blog
Tags: css, bootstrap, howto

Without any doubt, [Twitter's Bootstrap](http://twitter.github.com/bootstrap/)
is awesome. So far I am using it in more than 10 projects and I don't regret
anything.

Unfortunately, Bootstrap has one major flaw: You can't really add it to your
project and manipulate it, without editing the source files. Bootstrap offers
a download page where you can chose the parts that you want and where you can
enter values for all the variables - but I don't know who on earth works like
this. I usually don't know about exact color values for my project until
shortly before go-live and I certainly don't want to come back to the download
page and download new versions of bootstrap over and over again.

Here is what I want:

* I want to add Bootstrap to my project and work with the latest files from
  the github repo
* Yet I don't want to manipulate them, because
* I want to be able to update my bootstrap sources at any time without merge
  conflicts
* Updating should be a no-brainer

My solution might not be the most elegant, but so far it seems to get the job
done:


Add Bootstrap as a submodule
----------------------------

First I add bootstrap as a git submodule to my Django projects:

    git submodule add git://github.com/twitter/bootstrap.git myproject/submodules/bootstrap

It is important to add the submodule to a path inside your project root. This
way you can place symlinks easily with all relative paths.


Setup your css folder
---------------------

Surely you will have a folder that holds your project's CSS files somewhere in
your project. For my Django projects that is usually:

    myproject/myproject/static/css/

Inside of this folder I like to create a `libs` folder which holds CSS files
of third party plugins or frameworks that I use. In our case this would be
bootstrap, so let's create a bootstrap folder:

    mkdir myproject/myproject/static/css/libs/bootstrap/


Symlink the bootstrap files
---------------------------

So here is the first part of the trick. Inside of the `bootstrap` which we have
just created, we symlink all the `.less` files of the Bootstrap framework:

    cd myproject/myproject/static/css/libs/bootstrap/
    ln -s ../../../../../submodules/bootstrap/less/* .

It would be better to just symlink the whole `less` folder instead of all files
but unfortunately `lessc` is not able to follow such symlinks and would fail
to compile the `bootstrap.less` file.


Prepare the working files
-------------------------

Here comes the second part of the trick. We will create copies of the files
`bootstrap.less` and `responsive.less`:

    cd myproject/myproject/static/css/
    cp libs/bootstrap/bootstrap.less .
    cp libs/bootstrap/responsive.less .
    touch my-variables.less
    touch styles.less

I know, I know, we have just symlinked them, why create another copy now? The
reason is that we won't use the symlinks (you could delete them). Instead
we will make a three simple changes to those two files. First we need to change
the paths to all the imported `.less` files:

    sed -i -e 's/import "/import "libs\/bootstrap\//g' bootstrap.less
    sed -i -e 's/import "/import "libs\/bootstrap\//g' responsive.less

Next we will add an import of our own variables file to both files. The import
should come right after the import of the original `variables.less`:

    # Excerpt from your bootstrap.less copy:

    ...
    // CSS Reset
    @import "libs/bootstrap/reset.less";

    // Core variables and mixins
    @import "libs/bootstrap/variables.less";

    @import "my-variables.less"; // Our own variables overrides

    @import "libs/bootstrap/mixins.less";
    ...

Finally we will include our very own `styles.less` at the bottom of
`bootstrap.less`. Styles in this file would override everything else from
bootstrap:

    # Excerpt from your bootstrap.less copy:

    ...
    // Utility classes
    @import "libs/bootstrap/utilities.less"; // Has to be last to override when necessary

    // Our own stuff
    @import "styles.less";

Repeat the last two steps for `responsive.less` as well, of course here you
would add an import to `styles-responsive.less` instead of `styles.less` at the 
bottom.


How to work with this setup?
----------------------------

That's a whole lot of files to deal with, but the rules are actually quite
simple:

* Never touch anything in the `/libs/bootstrap/` folder
* If you would like to change the value of any of Bootstrap's
  [variables](https://github.com/twitter/bootstrap/blob/master/less/variables.less),
  override that same variable in our `my-varibales.less` file.
* You can even invent new variables here.
* Whenever you would like to add project specific styles for your site, add
  them to `styles.less` and `responsive-styles.less`.

When you are done, compile the files `bootstrap.less` and `responsive.less`. I
like to save the output as `bootstrap.css` and `bootstrap-responsive.css` and
those two files are the ones that I link in my templates.


Why is this awesome?
--------------------

First of all, you will have your project specific overrides included in the
rest of the Bootstrap framework and don't need to link it in your templates.
This saves you one request.

Secondly, we are symlinking to a git submodule, so if a new version or even
just a minor bugfix is released, we can just `cd` into the
`submodules/bootstrap` folder and run `git pull`. After that we need to
re-compile our files and that's it - we just updated our Bootstrap files.


What can go wrong?
------------------

There is one thing that can and will still go wrong: The two file that we have
modified and copied (`bootstrap.less` and `responsive.less`) might differ
when you pull the latest Bootstrap version. Especially when a major new release
happened, there will most definitely be new imports in those files. Luckily
those files are really simple, so you can probably spot the new import at a
glance. A new import would also mean that there is a new file that should be
symlinked.

So in this case, the best workflow would be this:

* Delete all symlinks and re-create them
* Copy `bootstrap.less` and `responsive.less` again
* Run the `sed` commands again
* Add the imports to `my-variables.less` and `styles.less` again.

You could even create a shell script for this task, therefore I consider it
a no-brainer :)


tl;dr
-----

We want to use bootstrap as a git submodule because then we can update it
simply via `git pull`.

We can't really touch any of the sourcefiles because that would result in merge
conflicts when we pull a new version, but the `variables.less` file is full of
gold and really needs to be changed.

As a solution, we just create our own `my-variables.less` file and import it
in copies of `bootstrap.less` and `responsive.less` - those files are just as
likely to change but if they do, we can re-create them in no time.
