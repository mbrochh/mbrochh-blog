Date: 2013-10-19
Title: Simple Backup With Rsync
Tagline: A Shell Script & Some Hardware to Backup Your Stuff
Slug: backup
Category: Blog
Tags: howto, shell, rsync, hardware

Every day I carry around about 830GB of data:

1. 80GB of application data and my home folder on a SSD drive in my MacBook
2. 440GB on the original MacBook HD which now serves as a secondary drive. It
   holds important documents, my iTunes and iPhoto libraries and other big
   files that I might need on a daily basis but don't want to put on my SSD
   drive.
3. Another 310GB on an external 500GB USB drive. It holds documents, pictures,
   music, movies, original Photoshop files, my Quake 3 Arena config (very very
   important!), downloads and all kinds of other files that have accumulated
   since I started using the internet in 1996. Losing this archive would be a
   real catastrophe.

So as you can see, my data is spread over three tiers:

1. Stuff I need every day. This must be fast. Therefore it sits on my SSD drive.
2. Stuff that I might need every day but that don't need to be very fast, such
   as music or files for ongoing projects. This is stored on the secondary
   drive.
3. Stuff that I will need when I am 90 years old and someone wants to write my
   biography aka my whole digital life. This doesn't need to be fast or
   convenient. Therefore it resides on the external USB drive.

The files on the SSD drive don't really need to be backed up. If my machine
explodes, I can buy a new one, clone my
[dotfiles from github](https://github.com/mbrochh/mbrochh-dotfiles), install a
few tools from the AppStore (XCode, Dropbox, Evernote, Skype, Pixelmator,
Alfred, Postgres.app) and I'll be up and running again within 3 hours or so.

What I do need to backup is the secondary drive in my MacBook and the external
USB drive. I thought a long time about this and browsed the internet for weeks.
I was searching for a good, reliable and affordable backup solution, but I
found none. Here are some options that I considered:

## Timemachine

First of all I don't want to lock myself into the Apple ecosystem. My backup
must be available from any hardware and OS and must not be tied to any kind of
software sorcery.

Secondly the internet is full of horror stories of users reporting how they
tried to backup from Timemachine and it either took a bazillion hours or failed
completely. Maybe these users are all idiots but maybe so am I.

Thirdly I don't need the go-back-in-time feature at all.  When was the last
time when you made a change to a file and suddenly though "Oh wait! This
document was much better last Thursday, let's go back in time!".  Even if I
wanted to do so: These documents would reside in git repositories and give me a
much more versatile way of going back in time.

Lastly I don't know how Timemachine does it's RAID system. I don't know how it
would warn me about drive failures. I don't know how I would proceed to replace
faulty drives. I don't know how to precisely manage which files to backup
and which not (because I never want a full backup). Just too many unknowns.
Dismissed!

## File Servers

The problem with professional NAS systems is: Their disks are expensive like
hell and they fail all the time. If you don't have enough money to replace
them, a second one will fail and your whole data goes to hell. Happened to a
friend of mine. Not cool. Apart from that, these things are big, noisy and eat
a lot of electricity. I also don't want to be able to SSH / FTP into my files
from remote locations, so with this this whole file server thingy I would
pay for a ton of features that I would never use.

## Cloud storage

Yea right. Because 1TB of cloud storage is something that we all can afford.
Besides, I don't want the NSA to have full access to my whole digital life.
I do have some files in an encrypted folder in my Dropbox (using
[Boxcryptor](https://www.boxcryptor.com/)). This makes sure that I can access
some important notes from anywhere in the world, but let's be honest, no one
needs access to all their terrabytes of data all the time from anywhere in the
world.

## Solution: rsync & a few drives

So here is my solution. I'm sure it is damn stupid and really inconvenient but
it was cheap and it allows me to sleep tight at night:

### Hardware

Disclaimer: The links below are Amazon Partner links. I'm not affiliated
with Western Digital or D-Link in any way and I didn't do a ton of research
before buying these. You might get to a much cheaper or much faster (USB 3.0?)
solution if you search a bit more.

1. [WD My Passport external HD 500GB](http://amzn.to/1eB0rY2) because I have
   always had great experiences with WD external drives. My last one lasted
   9 years and I can't say that I handled it with care.
2. [WD My Passport Carrying Case](http://amzn.to/1eB0GSE)
3. 2x [WD Elements Desktop External HDD 2TB](http://amzn.to/19ZSFaX), it's only
   USB 2.0 because USB 3.0 is too expensive and my MacBook doesn't support it
   anyways.
4. [D-Link DUB-H7 7 Port USB Hub](http://amzn.to/1c6h68m), because that's a
   whole lot of USB drives I have to connect when running a backup. And it's
   also pretty cool to have this hub when playing around with the Raspberry Pi
   ;-)

Total price: 245.12 EUR

### Software

I created a little bash script called
[backup.sh](https://github.com/mbrochh/mbrochh-dotfiles/blob/master/bin/backup.sh)
which I saved in my ``~/bin/`` folder. Therefore I can just type ``backup.sh``
into the terminal whenever I would like to run a backup. I can continue to use
the machine while the backup runs.

The script uses rsync, which is an awesome command line utility to keep two
folders in sync. It will take a long time on the first run, after that it will
only copy those files that have a changed last modified date. Note that I am
using the ``--delete`` flag. This means that when I delete a file in one of the
source drives, it will also be deleted on the destination drives.

### What does it do?

It's pretty simple: First the script copies all files from the secondary drive
and from the external USB drive to the first 2TB archive drive. Obviously that
drive should be larger than the other two drives combined. In my case it is
twice as large.

Now I have ALL MY DATA on one huge drive. This is good. But it would be a real
pain in the ass if this drive failed. Sure, I'd still have all the files on my
source drives but I would end up in a temporary state where I don't have any
backup until a new drive is shipped.

For this reason I just bought two of the 2TB drives and in the last step, I
simply mirror the first drive to the second drive. Here is another thing:
I store the second 2TB drive at a different location from the first and only
attach it once every month.

If our apartment burns down, 99% of my data will still be save on the second
drive and since I use it only once every month, I hope that it will not fail
anytime soon due to massive IO operations.

### What it doesn't do

It's not automatic. And it's not trying to be smart. When I delete files, they
will be gone from my archives as well. When I forget to run the backup on a
regular basis, I will be at risk to lose some data. When my computer blows up
and I actually need to retrieve data from the backup, I need to do that
manually.

### Is it future proof?

Currently the archive drives are twice as large as the source drives combined.
Therefore, if I buy a new MacBook with a bigger drive or a bigger external USB
drive, the archive drives will most probably still be able to hold all my data.

One (hopefully far away) day, after a few updates, the combined source drives
will be larger than the archive drives. This will be slight a hassle, but not
really a big problem: I would buy two new archive drives which would be
significantly larger than the old ones.

Then I'd mirror the old archive drive #1 to new archive drive #1. That's it.
After that I can run the script as usual and sell my old archive drives on
eBay.

The best thing is: The whole setup fits into my luggage, so for a nomad like me
this is also a solution that I can carry around with me, if I need to.
