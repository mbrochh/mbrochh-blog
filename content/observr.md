Date: 2013-05-28
Title: Observr
Tagline: Run Tasks Automatically on File System Changes
Slug: observr
Category: Blog
Tags: ruby, django, development

I have tried many file system watchers so far but none of them worked nicely
under Ubuntu and OSX with the same settings.

Recently I stumbled upon [observr](https://github.com/kevinburke/observr/)
which is a fork of the maybe better known but abandoned [watchr](https://github.com/mynyml/watchr).

Installation is super simple, just make sure that you have Ruby installed
and then run:

    #!sh
    gem install observr

If you are on OSX you should add:

    #!sh
    gem install ruby-fsevent

Now in my Django projects I usually have a super awesome [fabfile](https://github.com/bitmazk/django-development-fabfile)
which allows us to run two important tasks:

**fab check** will check the code for PEP8 compliance, then run the tests and
then check for 100% code coverage. If any of those fail, we can't commit our
changes, so its usually a good idea to run this all the time.

**fab lessc** re-compiles our style sheets from [less](http://lesscss.org/)
into `css`. Since we don't want to call this all the time in order to see our
changes in the browser, it is also a good idea to automate this. 

### Enter Observr

Observr simply watches the file system for changes and then executes a
command. Since our command is as simple as `fab check` or `fab lessc`, we can
build a very easy to read script. Just create a `compile-less.sh` file, and 
give it `chmod +x`, for example:

    #!ruby
    #!/usr/bin/env observr
    watch('.*less') { system('fab lessc') }

This would watch the filesystem for any changes in `*.less` files and then
execute the `fab lessc` fabric task. Make sure to activate your virtual
environment before running this script!
