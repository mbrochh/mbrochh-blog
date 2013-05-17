Date: 2013-05-17
Title: Shallow Copy Incidents
Tagline: How a Simple Bug Cost Me One Week of Sleep
Slug: copy
Category: Blog
Tags: python

I didn't sleep well recently. I'm one of the organisers of [PyCon SG 2013](https://pycon.sg)
and specifically it is my task to maintain the website. Since the conference
will be held very very soon, we are approaching a hot phase where everyone's
hard work has to come together nicely. Sponsors need to get verified, banners 
and T-shirts need to be printed, we need to publish our final logo, we need to 
get all tutorials and talks scheduled and make sure that our keynote speaker 
will have a smooth trip. And that's just the tip of the iceberg.

So in this exciting phase we need cash and in order to get cash, we need to
sell tickets and in order to sell tickets we better make sure that the PayPal 
integration on our website works.

You know it already: *Of course* the PayPal integration did *not* work properly
and that's what was keeping me awake during the last few nights. Today I 
cracked that nut and boy do I feel ashamed. This is one of the most epic fails
I have ever deployed.

I guess my constant work with the Django framework with all its tools and 
utilities has driven me so far away from Python's basics and internals, that I
finally couldn't see the tree in the forest any more. 

Here's a tale that is so embarrassing that it's almost funny again. Maybe
it will help someone else one day...

### Imagine...

Imagine the following code:

    #!python
    # file: setting.py
    DEFAULT_CHOICES = {
        'key1': 'foo' 
        'key2': 'bar',
    }


    # file: app.py
    form .settings import SOME_DICT

    class MyApp(object):
        def some_method(self):
            choices = DEFAULT_CHOICES
            if some_condition:
                choices.update({'key3': 'foobar'})
            self.some_other_method(choices)

This seems trivial, right? I have a setting with some default choices and in my
app I import that setting and based on some condition I sometimes want to add
some more extra choices to the set of default choices. Then I call another 
method that will do something with whatever choices it got.

This is basically what we are doing in our [Django PayPal Express Checkout app](https://github.com/bitmazk/django-paypal-express-checkout/blob/master/paypal_express_checkout/constants.py#L49).
We assemble some default values that should be sent to the PayPal API endpoint.
However, depending on the items the user choses to buy on the checkout form,
we add some more values to the dictionary and then send the whole thing to
PayPal in order to get the TOKEN from PayPal and finalise the payment.

This worked great. Our tests all passd, we got 100% code coverage, I even 
tested it in the browser against the live API when I bought my own conference 
ticket. 

Life was good. Until someone else wanted to buy a ticket.

### Hello, IT?

After my own purchase, everyone else got errors when trying to checkout for
payment. Luckily we have nice error logging in our PayPal module, so I could
see the response we got from the PayPal API:

> This Express Checkout session has expired. Token value is no longer valid.
> Error code: 10411

What the hell?! Have a look at the [line that caused the error](https://github.com/bitmazk/django-paypal-express-checkout/blob/c439b3c2c0698ebc61f1d5fc5c51856e5b12cab7/paypal_express_checkout/forms.py#L262).
`post_data` is supposed to contain some `DEFAULT_CHOICES` plus the post data
from the checkout form. And I'm pretty damn sure that we don't have any kind of
token in the checkout form, because, well, that form's main purpose is to ask
PayPal for a token, so we are totally not supposed to send any kind of token
here.

Yet, PayPal tells me that some mysterious token has expired.

No problem. We are doing IT here. When you don't know what else to do, you just
turn it off and on again, so I restarted the webserver and voila, people were
able to buy tickets again. Until it broke again, of course. So (please don't
laugh), what did I do? I added a cronjob which restarts the server every 30
minutes. If that's not the mother of all duct tape solutions, I don't know
what is. At least I could go back to sleep and we could collect some payments,
until of course it broke again.

Must. Try. Harder.

We are working with this PayPal module since a few months, even using it in 
production for four different projects. So keep that in mind when I'm telling
you that today I did something that I had never done before: 

I started my local devserver and bought *two tickets right after each other*. 
BAM! It even happened locally. I had never ever tried to buy two tickets in a 
row without restarting the devserver. When you think about it, this is quite
normal: You hack some code, then you start the website and see if the PayPal
checkout works. It does. Great. Back to writing code, restart the devserver, 
test again. Repeat. In all our apps, coming back within a short time and buying
again is simply not an option, so testing this scenario just never occurred to 
me. Shit.

### A Solution Dawns

The fact, that server restarts seemed to help was what kept my brain churning
during nights because I *knew* that it has to have something to do with imports
only happening at server start. It must be one of those errors that newbies
always do, when they want to define a default value for DateTime fields of
their Django models like so:

    #!python
    import datetime

    class MyModel(models.Model):
        start_date = models.DateTimeField(
             default=datetime.datetime.now(),
        )

You think whenever a new object is saved, the `start_date` will be set to now?
Forget it. It will be set to the time when the server was started, I hate this
bug. It's easy to overlook in code-reviews and will never really come to
surface during tests because you often wipe your database and usually deal with
fresh objects and most importantly, you restart the devserver all the time. It
will only bubble up when you do some important calculations on the `start_date`
and somehow all objects end up in all the wrong unexpected situations - only on 
production, of course.

To cut a long story short, what happened to me was exactly the same kind of 
beginner mistake. Remember:

    #!python
    from .settings import DEFAULT_CHOICES
    ...
    choices = DEFAULT_CHOICES
    choices.update({'key3': 'foobar'})

It turns out, the import happens only once at server start. And by assigning
`DEFAULT_CHOICES` to a variable I did not create a copy. I just created a 
pointer to the original variable. Therefore, when I call `update` on the
dictionary, I'm not only changing `choices` but also `DEFAULT_CHOICES` - my
evil persistent setting that got loaded on server restart and will remember
all changes made to it, even between different HTTP requests.

After more than 10.000 hours of Python programming I need to go back to the
basics and learn about [Shallow and deep copy operations](http://docs.python.org/2/library/copy.html).

In the end, the fix was [two lines of code](https://github.com/bitmazk/django-paypal-express-checkout/commit/67e9be786b29b1c2426416057fff595fd97110bb#L1R118)
that kept me sweating for almost a week:

    #!python
    from .settings import DEFAULT_CHOICES
    ...
    choices = DEFAULT_CHOICES.copy() 
    ...

**D'oh!**

Now go and buy those god damn [PyCon tickets](https://pycon.sg/checkout/) already, la!
