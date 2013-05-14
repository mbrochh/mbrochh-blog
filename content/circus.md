Date: 2012-07-13
Title: Daemonize Solr with Circus 0.5 on Webfaction
Slug: circus
Category: Blog
Tags: python, solr, circus

Since Webfaction increased the available memory from 40 MB to 250 MB I started
using Solr for more and more of my projects. However, I never really knew how
to ensure that Solr restarts itself if it crashes and how to easily stop and
start it in case I have to re-build the ``schema.xml`` file.

Then I found out about [Circus 0.5](http://circus.readthedocs.org/en/0.5/index.html)
and got curious.

Here is what I did to install zeromq, solr and circus on a Webfaction server:

## Install zeromq

Since we cannot install anything as root, I chose to install zeromq into
the folder ``/opt/zeromq-2.2.0``:

    mkdir -p $HOME/src
    mkdir -p $HOME/opt
    mkdir -p $HOME/etc
    cd $HOME/src
    wget http://download.zeromq.org/zeromq-2.2.0.tar.gz
    tar -xvf zeromq-2.2.0.tar.gz
    cd zeromq-2.2.0
    ./configure --prefix=$HOME/opt/zeromq-2.2.0
    make && make install

## Install Circus

Now we can install Circus. I assume that you are using virtualenv and
virtualenvwrapper:

    workon yourvenv
    pip install circus

This will fail because of the custom installation folder of zeromq. Thankfully
the failed zeromq build will remain in your virtualenv's build folder so that
you can install it again manually, this time giving it the path to your
zeromq installation:

    cd /your/Venv/
    cd build
    cd pyzmq
    python setup.py install --zmq=/home/username/opt/zeromq-2.2.0
    pip install circus

## Install Solr

Now let's install Solr, following [this post](http://django-haystack.readthedocs.org/en/latest/installing_search_engines.html#solr).
All you really need to do is download and unpack it:

    cd $HOME/opt
    curl -O http://apache.mirrors.tds.net/lucene/solr/3.5.0/apache-solr-3.5.0.tgz
    tar xvzf apache-solr-3.5.0.tgz

## Configure Circus

Create a `circus.ini` file somewhere on your file system. The following file
works great for me, just replace the path to your Solr installation
(usually just change your username):

    [circus]
    check_delay = 5
    endpoint = tcp://127.0.0.1:5555

    [watcher:solr]
    cmd = java
    args = -Djava.util.logging.config.file=logging.properties -jar start.jar
    working_dir = /home/<USERNAME>/opt/apache-solr-3.5.0/example
    warmup_delay = 0
    numprocesses = 1
    singleton = True

Start circus:

    circusd circus.ini &

That's it. On my Webfaction server circus eats 15MB RAM. You can now start and
stop Solr using `circusctl`:

    circusctl status solr
    circusctl stop solr
    circusctl start solr

Or try to kill Solr. Circus will immediately restart it:

    ps aux | grep java
    kill <solr PID>
    ps aux | grep java

You need to be careful when starting and stopping Solr. Even though Circus will
return ``[OK]`` the process will remain visible for a few seconds after you
stopped it. Similarly it will not accept requests for a few seconds after it
has been started. So if you use start and stop in a shell script or Fabric
task better insert some ``sleep`` seconds before doing anything else with Solr.
