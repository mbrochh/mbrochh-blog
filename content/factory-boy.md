Date: 2013-01-22
Title: Test Models with Generic Foreign Keys and Factory Boy
Slug: factory-boy
Category: Blog
Tags: python, django, testing, howto

Let's say you are writing a reusable Django app and your app has a model with
a generic foreign key. An example could be a messaging app where messages can
attached to any other object (when you think about Facebook, a message can
be sent to another User, or to his profile timeline, or to a status update
and so on):

    ::py
    class Message(models.Model):
        user = models.ForeignKey('auth.User')
        text = models.TextField(max_length=4000)
        creation_date = models.DateTimeField(auto_now_add=True)

        # Generic FK to the object this message is attached to
        content_type = models.ForeignKey(ContentType)
        object_id = models.PositiveIntegerField()
        content_object = generic.GenericForeignKey('content_type', 'object_id')

I like to maintain 100% code coverage in all my projects, so I will even test
seemingly mundane things like instantiation and saving of all my models. A test
for this `Message` model could look like this:

    ::py
    from django.test import TestCase
    from messages.tests.factories import MessageFactory

    class MessageTestCase(TestCase):
        def test_model(self):
            """Should be able to instantiate and save the model."""
            obj = MessageFactory()
            self.assertTrue(obj.pk)

Granted, this is a very simple test but as the model grows this test case would
obviously grow as well. The interesting question is: How can we write the
`MessageFactory`.

The first thought would be to just use one of our other existing models (i.e.
the Timeline model, if we were cloning Facebook). Unfortunately we can't do
that because we are writing a reusable app here and the reusable app should be
distributed on PyPi and therefore doesn't know anything about any of your other
app's models.

So we must create a `DummyModel` inside of our reusable app. You could put that
model into your reusable app's `models.py` but then you would create a useless
table when you run `syncdb` or `migrate`. So the better solution is to create
a `test_app` inside of your reusable app and only add that app to
`INSTALLED_APPS` in your `test_settings.py`.

So let's create a few new files:

    ::sh
    yourapp/tests/factories.py
    yourapp/tests/models_tests.py
    yourapp/tests/test_app/__init__.py
    yourapp/tests/test_app/models.py

Your test app's `models.py` should look like this:

    ::py
    class DummyModel(models.Model):
        name = models.CharField(max_length=256, blank=True)

Now we can create our reusable app's factory. There are three things to notice
here:

1. We will also create a factory for the `DummyModel` because then we can
   use it as a sub-factory. And who knows, maybe that model will get more
   complex as your app grows more complex as well.
2. We are using the [UserFactory of django-libs](http://django-libs.readthedocs.org/en/latest/factories.html#factories).
   django-libs is a collection of useful stuff that I need in almost all my
   Django projects. Obviously I need to create `User` instances all the time
   in my tests, therefore django-libs provides a `UserFactory`.
3. The `MessageFactory` uses the `content_object` field to add the generic
   foreign key to our `DummyModel`, which is quite convenient. Thankfully, we
   don't have to wrestle around with the `content_type` and `object_id` fields
   of the generic foreign key.

Here is how your `factories.py` should look like:

    ::py
    import factory
    from django_libs.tests.factories import UserFactory
    from yourapp.tests.test_app.models import DummyModel
    from yourapp.models import Message

    class DummyModelFactory(factory.Factory):
        FACTORY_FOR = DummyModel
        name = 'Foobar'

    class MessageFactory(factory.Factory):
        FACTORY_FOR = Message
        user = factory.SubFactory(UserFactory)
        text = 'Hello world'
        creation_date = factory.LazyAttribute(lambda x: now())
        content_object = factory.SubFactory(DummyModelFactory)

Now, whenever you want to create a `Message` in your tests, just call
`MessageFactory()` and there you are. Your message will be tied to an
instance of a `DummyModel` which will be created automagically as well.

One last problem is left: When you run your tests, you will get an error
message saying that there is no table for the `DummyModel` in your test
database. In order to solve this you should create a `test_settings.py` which
adds the `test_app` to your `INSTALLED_APPS`:

    ::py
    from myproject.settings import *
    INSTALLED_APPS.append('yourapp.tests.test_app')

Of course your `test_settings.py` needs a lot of other stuff. To speed up the
tests you could to change the db backend to an in-memory sqlite database and
for better test case recovery you could use a NoseTestRunner. Check out
my [test settings in django-libs](https://github.com/bitmazk/django-libs/blob/master/django_libs/settings/test_settings.py)
for an example that I use in all my projects.
