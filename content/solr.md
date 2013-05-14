Date: 2013-01-10
Title: Daemonizing Solr on Webfaction with Supervisor
Slug: solr
Category: Blog
Tags: solr, webfaction

A while ago I wrote how to [daemonize Solr on Webfaction with Circus ](http://martinbrochhaus.com/2012/07/circus.html).

Unfortunately this solution has not proven to be as stable as I wished, plus
I think there is a security issue because in theory other Webfaction users on
the same machine could communicate with my own Circus instance.

Today I tried to use [supervisord](http://supervisord.org/) for the first time.
Here is what I learned:


## Install supervisor on Webfaction

Kudos to [Jamie Curle](http://jamiecurle.co.uk/blog/webfaction-installing-configuring-supervisor/)
for describing the process nice enough for a dummy like me.

Following his instructions I made sure that I have not activated any
virtualenv, then I ran

    ::sh
    pip install supervisor

    # Let's create some folders we will need later on
    mkdir ~/tmp
    mkdir -p ~/mylogs/cron
    mkdir ~/etc && cd ~/etc
    vim supervisor.conf

Here is what my `supervisor.conf` looks like. Of course you would need to
insert your webfaction username and adjust the path to your solr installation:

    ::txt
    [unix_http_server]
    file=/home/username/tmp/supervisor.sock

    [supervisord]
    logfile=/home/username/mylogs/supervisord.log
    logfile_maxbytes=50MB
    logfile_backups=10
    loglevel=info
    pidfile=/home/username/tmp/supervisord.pid

    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

    [supervisorctl]
    serverurl=unix:///home/username/tmp/supervisor.sock

    [program:solr]
    directory=/home/username/opt/apache-solr-3.5.0/example
    command=java -Djava.util.logging.config.file=logging.properties -jar start.jar

The meaning of all these config sections should be obvious and is very well
documented in the [supervisor configuration documentation](http://supervisord.org/configuration.html).


## Enable solr logging

After having quite some trouble with solr being very instable, I decided to
figure out this whole logging thing. I found this little gem about
[solr logging](https://wiki.apache.org/solr/LoggingInDefaultJettySetup) which
made things very easy.

Just create the file `logging.properties` in the same folder where solr's
`start.jar` resides. Mine looks like this (again, replace username with your
webfaction account name):

    ::txt
    # Default global logging level:
    .level = INFO

    # Write to a file:
    handlers = java.util.logging.FileHandler

    # Write log messages in XML format:
    # Use java.util.logging.SimpleFormatter to log like Solr logs to the screen by default
    java.util.logging.FileHandler.formatter = java.util.logging.XMLFormatter

    # Log to the current working directory, with log files named solrxxx.log
    java.util.logging.FileHandler.pattern = /home/username/mylogs/solr%u.log

If you are wondering what different options for logging levels there are, have
a look at this page about [solr logging](http://lucidworks.lucidimagination.com/display/solr/Configuring+Logging).
`INFO` might be a bit too much if you are running a site where thousands of
users send hundreds of search queries per day - each query would be logged.


## Create crontab to restart supervisor

The last question is: Who watches the watchmen? Crontab does. Thankfully you
cannot run the `supervisord` command twice - it would warn you that another
instance is already running. Therefore we can safely schedule a cronjob to run
`supervisord` every five minutes:

    ::txt
    */5 * * * * ~/bin/supervisord > $HOME/mylogs/cron/supervisord.log 2>&1


## Manage solr

If you ever need to start, stop or restart solr, you can do so via
`supervisorctl start|stop|restart solr`.

You could also just run `supervisorctl` and would get into a manage console.
Then type `help` and see what commands are available. There seems to be an
[open bug](https://github.com/Supervisor/supervisor/issues/121) with the
`reload` command at the moment, so better don't use that one for the time
being.


## Bonus: Fabfile to rebuild the index

Every now and then you will introduce changes to your models and your search
index that will require a rebuild of the index. I like to automate that with
a Fabric task. Here it is:

    ::py
    def run_rebuild_index():
        """Rebuilds the Solr index on the server."""
        run('supervisorctl stop solr')
        time.sleep(5)
        run('workon envname && $HOME/webapps/django/myproject/manage.py build_solr_schema > $HOME/opt/apache-solr-3.5.0/example/solr/conf/schema.xml')
        run('supervisorctl start solr')
        time.sleep(5)
        run('workon envname && $HOME/webapps/django/myproject/manage.py rebuild_index --noinput')
