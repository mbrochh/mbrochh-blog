Date: 2012-10-13
Title: Deploying Barkeep on Linode from OSX
Slug: barkeep
Category: Blog
Tags: git, codereview, ruby, barkeep
Status: draft

* Create new Linode with Ubuntu 10.04 LTS 32 Bit
* `cd ~/Repos`
* `git clone git://github.com/ooyala/barkeep.git && cd barkeep`
* `cp config/deploy_targets/vagrant.rb config/deploy_targets/my_company.rb`
* Change `my_company.rb`

* bash < <(curl -s https://raw.github.com/wayneeseguin/rvm/master/binscripts/rvm-installer)
* add to .bash_exports: [[ -s "$HOME/.rvm/scripts/rvm" ]] && . "$HOME/.rvm/scripts/rvm"
* rvm install 1.9.3-p194
* gem install bundler
* j barkeep
* set terraform (0.0.6) in Gemfile.lock
* bundle install
* comment out integration tests in config/tasks/deploy.rake (159)

* ssh into server
* create .ssh/authorized_keys file
* sudo apt-get update
* sudo apt-get install rsync git-core build-essential ruby

* bundle exec fez bitmazk deploy --trace
* script hangs when installing ruby, aborted and re-run / watch on server with ps aux
* bundle exec fez bitmazk deploy --trace

Secure site:
* cd /var/www/
* mkdir barkeep && cd barkeep
* sudo apt-get install apache2-utils
* htpasswd -c /var/www/barkeep/.htpasswd yourusername
* vim /etc/nginx/sites-enabled/barkeep.conf
* add to location / at the bottom:
  auth_basic "Restricted";
  auth_basic_user_file /var/www/barkeep/.htpasswd;
* /etc/init.d/nginx reload
* follow linode docs to secure site
