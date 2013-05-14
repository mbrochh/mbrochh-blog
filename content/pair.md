Date: 2012-05-26
Title: Secure pair programming with wemux and Vim
Slug: pair
Category: Blog
Tags: screen, tmux, wemux, vim, ssh, programming

At [Bitmazk](http://www.bitmazk.com) we are a small team of web developers
with members located in Singapore and Germany. Of course we do codereviews
with Google's awesome [Rietveld](https://code.google.com/p/rietveld/) but
often when someone has an immediate problem, pair programming is just so much
more efficient.

We used to use Skype for talking and Teamviewer for screen sharing, which
worked very well for a while but after recent updates both tools became so
unreliable that they started affecting our work. More importantly: Even when
those tools worked perfectly well there is significant lag between what I say
and what my coworker sees. It's just not an optimal solution for staring at a
terminal.

I first tried to set this up with GNU Screen and it almost worked but at the
final step I ran into a dead end. It seems as if
[multiuser support on OSX 10.7 is broken](http://superuser.com/questions/117684/gnu-screen-multiuser-mode-is-broken-in-os-x-10-6-snow-leopard).
Or maybe I was just too stupid to get the permissions for the guest user right. 

As a last resort I tried to achieve my goal with
[wemux](https://github.com/zolrath/wemux). It worked right out of the box and
took me less than 5 minutes to setup. Goodbye GNU Screen, I guess.

The process I am going to describe here looks complex but it is really really
simple. Please don't give up here!

1. Setup a new user ``pairprogger``
2. Authorize your colleagues to ssh into that user's account
3. Setup port forwarding in your router's settings
4. Enable remote login (OSX) / start an openssh-server (Ubuntnu)
5. Install tmux and wemux
6. Start a wemux server
7. Join a wemux server

It will blow your mind even more if you had two machines at your disposal but
you will of course be able to test this with just one machine and two
terminals.

But rest assured that you won't be able to sleep until you find a real person
on the internet who you can show this little trick. You have been warned. ;)

## Step 1: Create a guest user account

You will ask your colleagues to ssh into your machine for pair programming.
When I set this up I didn't bother about security at first as I just wanted
to see how this feels. I invited a very close friend of mine to test this
and I can tell you that it feels weird. You really don't want anyone in your
machine with access to your whole home folder. Especially not if he is a
hacker. At least I could come up with a dozen evil pranks immediately...

So let's create a new user called ``pairprogger``. For OSX I have created a
file ``create_user.sh``. Replace the three variables at the top and execute it.

**OSX**

    # find out your staff group id (for me it is 20)
    # dscacheutil -q group
    STAFF_GROUP_ID=XX
    USERNAME="pairprogger"
    PASSWORD="yourpassword"

    MAXID=$(dscl . -list /Users UniqueID | awk '{print $2}' | sort -ug | tail -1)
    NEWID=$((MAXID+1))

    sudo dscl . -create /Users/$USERNAME
    sudo dscl . -create /Users/$USERNAME UserShell /bin/bash
    sudo dscl . -create /Users/$USERNAME UniqueID "$NEWID"
    sudo dscl . -create /Users/$USERNAME PrimaryGroupID $STAFF_GROUP_ID
    sudo dscl . -create /Users/$USERNAME RealName "Pair Programmer"
    sudo dscl . -create /Users/$USERNAME NFSHomeDirectory /Users/$USERNAME
    sudo dscl . -passwd /Users/$USERNAME $PASSWORD
    sudo dscl . -append /Groups/com.apple.access_ssh GroupMembership $USERNAME
    sudo createhomedir -c -u $USERNAME
    # make sure that there is /Users/pairprogger/ on your disk now

I wont take credit for this insane user creation script for OSX.
This thread on serverfault about
[how to create a user account on OSX](http://serverfault.com/questions/20702/how-do-i-create-user-accounts-from-the-terminal-in-mac-os-x-10-5)
certainly saved my ass.

**Ubuntu**

    sudo useradd -m -s /bin/bash pairprogger
    sudo passwd pairprogger

You should be able to test this by logging out. The new user should appear
on your login screen.

## Step 2: Restrict access via public RSA keys

You know the password of ``pairprogger`` but you are not going to give it
away, as it cold get leaked and all kinds of people would be able to ssh into
your machine. Instead you will create a ``.ssh`` folder for the new user
and paste your colleagues public RSA keys into the ``authorized_keys`` file:

**OSX / Ubuntu**

    su - pairprogger
    mkdir .ssh
    chmod 700 .ssh
    cd .ssh
    touch authorized_keys
    chmod 600 authorized_keys

Now copy the public RSA keys of the users you want to work with into the
`authorized_keys` file. You might want to add your own key as well in order
to test your setup later.

## Setp 3: Enable port forwarding

There are certainly more elegant solutions where you tell your router that
this computer should _always_ get that IP and where you setup dyndns and all
but I will describe a simpler approach here. Of course the drawback is that
your IP will change all the time and every day you might have to repeat these
steps.

Note down your [public IP](https://duckduckgo.com/?q=ip)

Note down your local IP:

**OSX**

    ipconfig getifaddr en1

**Ubuntu**

    ifconfig wlan0 | grep 'inet addr' | sed 's/.*inet addr:\([0-9.]*\).*/\1/'

To setup port forwarding go to `192.168.0.1`. This IP might differ on your
router. Usually you should find a section for advanced settings which should
have a section for port forwarding or just forwarding. You should see a table
where you can enter your machine's local IP address and define which ports
should be forwarded. You should forward port 22 for SSH and 8000 for your
Django development server. The latter will enable you to do some pair
programming and then have a look at the result together, each worker in their
own browser.

## Step 4: Enable remote access

Next you should start your local ssh server so that people can actually ssh
into your machine. If anyone knows how to do this on the command line in OSX,
please let me know in the comments! On Ubuntu I just had to install
``openssh-server`` and it worked immediately. We will be extra paranoid here
and restrict access only to the ``pairprogger`` user and we will disallow
password authentication, which would allow people to crack your password
via bruteforce.

**OSX**

Go to `System Preferences` --> `Sharing` --> `Remote login`. Add
`Pair Programmer` to the list `Allow access for`.

    sudo vim /etc/sshd_config
    # Set PasswordAuthentication to no
    # Set ChallengeResponseAuthentication to no
    # Set UsePAM to no

**Ubuntu**

    sudo apt-get install openssh-server
    sudo vim /etc/ssh/sshd_config
    # Set PasswordAuthentication to no
    # Add the following to the bottom of the file:
    # AllowUsers pairprogger

Please note that I am not a security expert. I have added these ssh
restrictions while writing this post and have not tested them thoroughly. It
would probably be a good idea to also make sure that the user ``pairprogger``
is not allowed to leave his home folder and give him some quota so that he
cannot flood your hard drive with porn. If anyone knows useful settings to
further restrict this account, please leave them in the comments.

So this was the hard part. Now to the fun part...

## Step 5: Install tmux and wemux

Since wemux seems to be based on tmux, you need to install both, but that
should be a no-brainer:

**OSX**

    brew install wemux
    brew install https://github.com/downloads/zolrath/wemux/wemux.rb

**Ubuntu**

    sudo apt-get install tmux

On Ubuntu follow the instructions at https://github.com/zolrath/wemux for
manual installation.

## Step 6: Start the wemux server

You are ready to go. Type the following command:

    wemux start

## Step 7: Join the wemux server

Now tell your friend to join you:

    ssh pairprogger@your-public-ip
    wemux attach

## Bonus: Your first tmux config

If you used GNU screen and if you are a Vim user, you will most likely find the 
settings in my [.tmux.conf](https://github.com/mbrochh/mbrochh-dotfiles/blob/master/.tmux.conf)
very useful.

I hope I didn't forget anything. If so, please let me know in the comments!

Oh and: This is how it is going to look like:
![wemux server](./images/wemux.png)

Note how wemux determines that my Ubuntu machine has lesser screen resolution
and automatically scales down the working area on my MacBook. If this is not
awesome...
