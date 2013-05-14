Date: 2012-06-08
Title: PyCon APAC 2012 - Keynote
Slug: eafp
Category: Blog
Tags: python, pycon, conferences

Here are my live notes on [Alex Martelli's](https://plus.google.com/106273672060692715136/about)
keynote "Permission for Forgiveness".

_Edit_: Here is the video: https://www.youtube.com/watch?v=lEtyYEKqUlk

He starts with a joke about the font in his presentation which looks like
Comic Sans but is actually Apple's Chalkboard.

We learn about [Grace Hopper](https://en.wikipedia.org/wiki/Grace_Hopper) who
ironically won the first "CS _man_ of the year" award in 1969. Alex talks a lot
about her many achievements, one remarkable story is how she _caught_ the first
[computer bug](https://en.wikipedia.org/wiki/File:H96566k.jpg) in the Mark I.

This is fantastic! I always knew about the story why bugs are called bugs but I
never knew about this image of the actual first bug being filed.

[EAFP](http://docs.python.org/glossary.html#term-eafp) means "Easier to ask
forgiveness than permission" and it was Hopper's secret recipe for being
successful and innovative inside a huge and bureaucratic organization (the
Navy). Now that I found this reference in the Python glossary I'm beginning to
understand why this is a good keynote for a Python conference :)

# Why does EAFP work?

* If you ask for permission, the bureaucrat is likely to deny it, because it
  might just be the easiest thing for him to do and because he might see
  approval as a risk for his own career, since he needs to take responsibility
  for something he probably only remotely understand.
* The bureaucrat is more likely to grant forgiveness since again, this would
  be the easier thing for him to do, especially if the project turned out to
  be successful.

# EAFP and Python

Alex gives a nice example of reading files. Many people (me included, shame on
me) would first check if the file exists and then access the file. However,
this is really stupid because one second after your check another process might
just delete the file and renders your check worthless. Better just read the
file and capture any exception. Or in other words, ask for forgiveness.

Another common example is the ``hasattr`` call. Python often has defaults,
so you could just as well just call ``getattr`` and return a default if
the attribute cannot be found.

# EAFP in software

Interesting example. [Optimistic concurrency](https://en.wikipedia.org/wiki/Optimistic_concurrency_control):
Instead of creating blocks of code that are protected by locks (asking for
permission), just do it, but have means to detect if the object you are working
on, has been changed while working, also make sure that your work is in a
transaction that can be reversed. Now, if the object changes while you are
working on it, just rollback and try again. This is very common with relational
databases and I really wonder how this could be implemented when working with
Python objects.

Source control is another example. In most modern version control systems you
can just push your code and the system will try to just do it and ask for your
help if someone else pushed just before you. Ironically Microsoft's Visual
Source Save locks files (at least a few years ago when I last worked with it).
How fitting for a large bureaucratic organization.

# EAFP in startups

At least for modern tech startups, the agile approach has clearly won. Just
launch a beta of your software as quickly as possible and see what happens.
When I think about it, Facebook clearly follows this model and shoots first,
asks for forgiveness later. Well... actually they never really ask for
forgiveness, I think :)

# Considerations

You shouldn't do EAFP everywhere and all the time. Where there are rules that
make sense and that have protocols attached to them that make it possible to
actually work with the rules, you should, obviously, follow them.

Highly security relevant systems might be an example where EAFP would be rather
harmful.

EAFP is not a license to do evil and ask for permission later.

# Conclusion

Great keynote for a PyCon. I like the general theme and idea to just go ahead
and do things, as long as you don't do evil. It's also kind of encouraging to
try to stand out even when facing seemingly impossible to overcome bureaucratic
barriers.

Slides can be found [here](http;//www.aleax.it/pycon12ap_fop.pdf)
