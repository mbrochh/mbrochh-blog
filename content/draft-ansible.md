Date: 2014-01-08
Title: Django, Vagrant & Ansible
Tagline: Privisioning Django boxes with Vagrant and Ansible
Slug: ansible
Category: Blog
Tags: python, django, vagrant, ansible
Status: draft

Let's say you have a complex Django application under version control and some
day some designer wants to jump on board and work on the project. Let's also
assume that designer is a great artist but doesn't really care about software
development, so his machine doesn't have all the dependencies needed to run
your complex Django app (Postgres? Memcached? Redis? Solr?).

VirtualBox, Vagrant and Ansible can be of great help in this situation. Those
three tools are extremely easy to install on OSX or Ubuntu.


# Installation

1. Download and install Virtualbox
2. Download and install Vagrant


# Django project setup

CD into your Django project's root folder and create a `Vagrantfile`:

    #!sh
    $ cd ~/projects/my_django_project/src/
    $ vagrant init precise32 http://files.vagrantup.com/precise32.box

This creates a `Vagrantfile` and sets operating system and image download path. 

    #!sh
    $ vagrant up

This executes the `Vagrantfile`. It will realise that there is no box with the
name `precise32`, yet so it will download it and store it at a folder that is
managed by Vagrant. In the future, if you want to use a box with the name
`precise32`, it will not be downloaded again. Vagrant will never touch these
boxes and only use them to clone them as a starting point for your VMs.
The box will be stored at `~/.vagrant.d/boxes/precise32/virtualbox/` and take
about 282MB disk space.

Set the following line in the `Vagrantfile`:

    #!txt
    config.vm.network :private_network, ip: "192.168.111.222"

This will give the machine the given IP. We will later need that IP for our
Ansible playbook.

Add `vagrant_ansible_inventory_default` to your .gitignore. This folder get's
created automatically by Vagrant. It allow you to use the inventory group
with the name `default` in your Ansible playbooks.

Uncomment the following line in the `Vagrantfile` and change the ports:

    #!txt
    config.vm.network :forwarded_port, guest: 8080, host: 8081

This is because on the VM (guest) we will execute the django development server
which usually runs on port 8080. On your host machine, we will then access
the website in the VM via `localhost:8081`.

SSH into the box via

    #!sh
    $ vagrant ssh

Your Django project directory (the one with the `Vagrantfile`) is a synced
folder in the VM, so you can CD into it:

    #!sh
    $ cd /vagrant
    $ ls

You will see your Django project. So now you are able to work on the project
on your local machine and all changes will be reflected in the VM as well.
