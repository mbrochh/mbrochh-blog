Date: 2014-05-06
Title: PasswordMaker Online
Tagline: How to use the best password manager in the world
Slug: passwordmaker
Category: Blog
Tags: technology, security, privacy, tools

It must be more than six years that I am using
[PasswordMaker](http://www.passwordmaker.org/passwordmaker.html) to manage all
my passwords. I think this is the best password tool that could ever exist.
Unfortunately it is a little bit difficult to understand and a little bit
inconvenient to use, but when it comes to cryptography, there is always a
tradeoff between convenience and security: You can't have both at the same
time.

So what do I need from a good password manager?

1. It must enable me to have a unique password for every service that I use
2. It should be available on all devices that I use
3. It must not need any kind of user account with any kind of company
4. It must not store my passwords anywhere
5. It must not communicate with any API any time
6. I only want to remember one master-password
7. Bonus: I should still be relatively save even if someone knows my master password

## How does it work?

It is very simple: The browser extension (available for
[Chrome](https://chrome.google.com/webstore/detail/passwordmaker-pro/ocjkdaaapapjpmipmhiadedofjiokogj?hl=en)
and [Firefox](https://addons.mozilla.org/en-US/firefox/addon/passwordmaker/))
takes the domain of the site in your active tab and concatenates it with your
master password. Let's say you are looking at `google.com` and your master
password is `abc123`, then the resulting string would be
`google.comabc123`.

PasswordMaker takes that string and applies a Hash algorithm on it. The default
is MD5 but you can change that if you like. So the resulting password could be
`z4En5AWL` for `google.com` and `CcUgOJIA` for `dropbox.com` and so on.

So if you want to fill out a password field on the web, you just open the
extension and the top-level domain will already be filled out. You enter your
master password and then click a button to insert your password into the
password field. Alternatively you can copy the password into the clipboard and
it will be removed from the clipboard after 10 seconds or so.

## Here are some important tips

1. Change the hash algorithm to something else than MD5.
2. Change the password length to something else than 8. Make it as long as
   possible. 16 characters should be good.
3. Change the allowed character set to characters and numbers only, because
   some services out there don't allow special characters.
4. If you want to be really nasty, disallow any random character.
5. Apply a prefix of `aA1!` - this makes sure that no matter how random your
   password is, you will ALWAYS have at least one minor letter, one capital
   letter, one number and one special character. Some fucking annoying websites
   out there enforce this stuff.

Note: Be careful about this. You usually only set your settings once and after
that you don't really care about them any more. This something you could easily
forget and if you find yourself in front of a new PC one day and need to
set everythign up again, you don't want to forget those old settings. In the
wors case, you have to come up with new settings and re-set all your passwords.

## What do I do on mobile?

There is an [Android app](https://play.google.com/store/apps/details?id=org.passwordmaker.android)
and an [iOS app](https://itunes.apple.com/us/app/passwordmaker.org-password/id359001896?mt=8).

## What do I do when I'm on a public computer?

One day you will need one of your passwords and you don't have your phone with
you and the browser on that machine doesn't have the extension installed.

No problem! You can always fall back to visiting the
[PasswordMaker website](http://www.passwordmaker.org/passwordmaker.html)
which is slightly inconvenient, because you have to set all your settings
first. Can't remember that URL? Google for `passwordmaker online`!

## What do I do with passwords for offline apps?

Your browser with it's extension is always just a click away. Just open the
extension and instead of a top level domain enter the name of the app you want
to authenticate with.

## What do I do when I have several accounts with the same top level domain?

Same thing: Open the extension and append something to the top level domain.
I have many Googlemail accounts, so I would turn the top level domain into
something like `google.com/mbrochh`.

## But can the PasswordMaker website be trusted?

Nothing on the web can be trusted. Download the website and audit it's code.
Then put it on a USB stick and use your own version. Besides - you can open
the website, then disable your internet connection. It will still work. All
the magic happens via JavaScript on your client only. At no time will anything
you enter into that form be sent over the wire.

I downloaded the website and host [my own copy at Github](http://mbrochh.github.io/passwordmaker/).

## Re-cap: How does PasswordMaker solve the problems mentioned initially?

> 1) It must enable me to have a unique password for every service that I use

Check! Since all your accounts are hosted on different websites, which means
different top level domains, the hash algorithm will generate different random
passwords for each domain. This means that all your passwords will be unique.

> 2) It should be available on all devices that I use

Check! There are extensions for Firefox and Chrome. By the way, this is the
main reason why I will never use Safari. That browser has the worst extension
ecosystem ever and it is basically impossible to surf the web in any reasonably
safe way. There are apps for Android and iPhone. That's all I'll ever need.

> 3) It must not need any kind of user account with any kind of company

Check! You don't need to create any account. You can download the PasswordMaker
static website. I don't see why there would ever be updates to the website.
website and put it on your Github account and host it yourself. It's just a

> 4) It must not store my passwords anywhere

Check! See the beautiy of it? The master password is in your head and the rest
is created on the fly. No password is ever stored anywhere (except when you
enable to save your master password in your RAM during a browser session).  I
do that. If my adversaries are so powerful that they can read my RAM at any
time, I'm fucked anyways.

> 5) It must not communicate with any API any time

Check! Neither the mobile apps nor the browser extension nor the original website
need an internet connection.

> 6) I only want to remember one master-password

Check! Well, almost. If you make a lot of changes to your default settings,
you also need to remember those. I have a really really bad memory, but somehow
I can always remember my settings.

> 7) Bonus: I should still be relatively save even if someone knows my master password

Check! Even if someone manages to get your master password through social
engineering or a key-logger or by placing a smartphone on the table next to
your laptop and listening on the sound of your keystrokes (this shit is really
scary, ain't it?), they would still need to know the username and he exact
settings for your PasswordMaker profile in order to sneak into your accounts.

If you have applied all the tips I mentioned above, even with the knowledge of
your master password (and the knowledge that you use PasswordMaker at all) it
should be very very hard to bruteforce into your account.

That's it. If you are using anything else for your passwords, you are doing it
wrong. There. I said it.
