Date: 2013-10-19
Title: My Simple Backup Solution
Tagline: A Shell Script & Some Hardware to Backup My Stuff
Slug: backup
Category: Blog
Tags: howto, shell, rsync, hardware 

Every day I carry around about 830GB of data:

1. 80GB of application data and my home folder on a SSD drive in my MacBook
2. 440GB of Documents, my iTunes Library and my iPhoto Library on the original 
   drive that came with my MacBook and is now the secondary drive
3. Another 310GB of documents, pictures, music, movies and files that I just
   can't delete on an external USB drive. The files on this drive have been
   accumulated over the last 15 years or so and losing them would be a real
   catastrophe.

Since disk space on the MacBook is quite limited, I'm using the external USB
drive (500 GB) as an extension for the builtin drives. Think of it as my file
archive.

The files on the SSD drive don't really need to be backed up. If my machine
explodes, I can buy a new one, clone my 
[dotfiles from github](https://github.com/mbrochh/mbrochh-dotfiles), install a
few tools from the AppStore (XCode, Dropbox, Evernote, Skype, Pixelmator,
Alfred, Postgres.app) and I'll be up and running again within 3 hours or so.

What I do need to backup is the secondary drive in my MacBook and the external
USB drive. I thought long about this and browsed the internet for weeks,
searching for some good, reliable and affordable backup solutions, but I found
none. Here are some options that I considered:

## Timemachine

TODO: Why did I not like Timemachine?

## Fileservers 

The problem with RAID systems is: Their disks are expensive like hell and they 
fail all the time. If you don't have enough money to replace them, a second one 
will fail and your whole data goes to hell. Happened to a friend of mine. Not 
cool. Apart from that, these things are big, noisy and eat a lot of 
electricity.

## Cloud storage

Yea right. Because 1TB of cloud storage is something that we all can afford.
Besides, I don't want the NSA to have full access to my whole digital life.
I do have some files in an encrypted folder in my Dropbox (using 
[Boxcryptor](https://www.boxcryptor.com/)). This makes sure that I access some
important notes from anywhere in the world, but let's be honest, no one needs
access to all their terrabytes of data all the time from anywhere in the
world.

## Solution: rsync & a few drives

TODO: Describe solution
