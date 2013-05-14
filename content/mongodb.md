Date: 2012-06-08
Title: PyCon APAC 2012 - MongoDB with Python
Slug: mongodb
Category: Blog
Tags: python, pycon, conferences

Here are my notes on [Mathias Stern's](https://twitter.com/#!/mathias_mongo)
talk about "MongoDB with Python"

_Edit_: Here is the video: https://www.youtube.com/watch?v=hU8rkNT6CVk

MongoDB should make your life easier. You should be able to start coding
as fast as possible.

Starting the database is as simple as creating a ``~/mongodb/data/`` folder
and starting ``mongod`` giving it that path to the desired db folder.

Every object has an ``_id`` attribute. The id's are of type ``ObjectId`` which
are similar to UIDs.

Creating objects is very simple:

    ::py
    import pymongo
    from bson import ObjectId

    # TODO create connection

    post = {
        '_id': ObjectId(),
        'author': 'mathias',
        'body': 'I wrote something',
        'title': 'My First Post'
    }
    db.posts.save(post)

Finding is similar:

    ::py
    pprint(db.posts.find_one({'id": post['_id']}))
    # or
    for post in db.posts.find():
        pprint(post)

Note that there is no schema at all. We can start doing this right away, no
need to define any tables or something. We also don't need to alter tables
to add new columns. We would just save or update a post that has the new
column. Now we would have two kinds of posts in the database: Some have the
new column and some don't.

From here on there was too much shown to keep up with taking notes.
Overall it seems to be very very simple and straightforward to work with
MongoDB. I shall try it out in a future project.

The presentation was done in [Ipython Notebook](http://ipython.org/), which
seems to be an awesome tool for tinkering around with new APIs.

Some links:

* [pymongo](http://pypi.python.org/pypi/pymongo/)
* [BSON](http://bsonspec.org/)
