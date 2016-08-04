Date: 2016-08-04
Title: Using Letsencrypt on Digital Ocean
Tagline: Just a note to myself...
Slug: letsencrypt
Category: Blog
Tags: ssl, server

First of all, DigitalOcean has a
[pretty good official guide](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04)
for this.

However, I still struggled a bit with that guide, so here are my notes:

First we need to login as root and install Letsencrypt:

```
sudo git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt
```

Next we need to make sure that nginx is configured so that the
`/.well-known/...` URL can be accessed. Note: I typically have a non-root
user `django` on my servers, that's why I set the `root` directive to a folder
under that user's account. Make sure that the folder
`/home/django/www/letsencrypt/.well-known` exists (by logging in as that user
and creating it).

```
server {
    listen 80;
    server_name example.com;
    root /home/django/www/letsencrypt;

    location / {
        rewrite ^ https://example.sg$request_uri? permanent;
    }

    location ~ /.well-known {
        allow all;
    }
}
```

Next we need to obtain our certificate for the first time:

```
/opt/letsencrypt/letsencrypt-auto certonly -a webroot --webroot-path=/home/django/www/letsencrypt -d example.com
```

A blue screen will appear, asking for your email address and if all goes well,
the certs will placed at `/etc/letsencrypt/live/example.com`.

Hint: If you were already using a cert, possibly even one from letsencrypt,
you might need to delete the `/etc/letsencrypt/` folder and comment out
the SSL part in the nginx conf.

Now configure nginx to actually use the certs:

```
server {
    listen 443 ssl;
    server_name example.com;
    root /home/django/project_assets;

    ssl on;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;

    ...
}
```

And reload nginx:

```
sudo service nginx reload
```

Finally, let's automate the renewal:

```
mkdir /root/bin
mkdir /root/log
touch /root/bin/renew-ssl-cert.sh
chmod +x /root/bin/renew-ssl-cert.sh
```

Put the following code into `renew-ssl-cert.sh`:

```
/opt/letsencrypt/letsencrypt-auto renew > /root/log/letsencrypt-auto.log 2>&1
sudo service nginx reload
```

And add the following line to crontab:

```
* 1 * * 1 /root/bin/renew-ssl-cert.sh > /root/log/renew-ssl-cert.log 2>&1
```

You might want to test if everything works:

```
/root/bin/renew-ssl-cert.sh > /root/log/renew-ssl-cert.log 2>&1
```

It should create two files in `/root/log`:

```
-------------------------------------------------------------------------------
Processing /etc/letsencrypt/renewal/example.com.conf
-------------------------------------------------------------------------------

The following certs are not due for renewal yet:
  /etc/letsencrypt/live/example.com/fullchain.pem (skipped)
No renewals were attempted.
```

and:

```
* Reloading nginx configuration nginx
   ...done.
```

I hope this helps :)
