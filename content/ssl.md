Date: 2012-06-13
Title: Installing Free SSL certificate with StartSSL and Webfaction
Slug: ssl
Category: Blog
Tags: ssl, webfaction

For my next big project it will be mandatory to use a SSL certificate for the
web application. I have never dealt with SSL before, so I am going to take
some notes here. Let's see how it goes...

I chose [StartSSL](https://www.startssl.com/) because they offer a free
certificate.

I had to provide my name, address, phone number and email. After that I got an
activation link immediately. Interestingly I don't have to authenticate myself
on the StartSSL website via username and password. Instead they installed a
client certificate in my browser, which I exported and securely saved in my
Dropbox account, in case that I reinstall my system in the future.

From here on it is just following a wizard to create a new certificate for a
new domain. After following all instructions given by the wizard, I ended up
with a bunch of file (.crt, .pem, .key) which I all copied into my Webfaction
server, as described in the [SSL docs at Webfaction](https://docs.webfaction.com/user-guide/websites.html#secure-sites-https).

I opened a support request in my Webfaction account and asked for activation
of the certificate. In the meantime I created another website in the control
panel that uses HTTPS and maps the same apps as the non-HTTPS version.

Just a few minutes after opening the support ticket I got a friendly response
from the Webfaction support telling me that everything worked fine and indeed,
I can now access my website via HTTPS.

Wow. That was easy! The whole process took me less than an hour to setup.
I'm going to use SSL for all my sites from now on.
