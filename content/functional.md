Date: 2012-06-08
Title: PyCon APAC 2012 - Functional Programming in Python
Slug: functional
Category: Blog
Tags: python, pycon, conferences

Here are my notes for [Gavin Bong's](https://twitter.com/chihiro)
talk about functional programming in Python.

_Edit_: Here is the video: https://www.youtube.com/watch?v=r75X4Vn_E9k

Sorry for the horribly weird notes. I don't know anything about functional
programming and got lost during the talk more than once. :/

Gavin describes key features of functional programming. Given the common
definition for functional languages, Python is _not_ a functional language.

However, it provides many features of functional languages, like immutable
containers (tuple, forzenset) or lambda functions. Unfortunately Python
lambdas can only contain a single expression.

Good to know: Gavin used Haskell to teach himself functional programming...
that's what I tried as well a few months ago. I guess I should pick it up
again.

# High order functions

These are functions that accept other functions as parameters. Python has some
built-in functions that heavily rely on this:

* map
* filter
* reduce

An alternative to filter would be list comprehensions, which also have a
similar syntax to Haskell.

# Recursion

Functional languages do not have looping constructs. They use recursion
instead, which of course can be done in Python as well. The problem is that
Python needs to maintain the stack frame for each recursion, so you can easily
end up with a stack overflow when doing naive recursion. Many functional
languages optimise this by reusing the stack frame (Tail Recursion
Elimination).

Python cannot do this because it would result in useless stack traces and make
debugging too hard.

It seems as if this can somehow be emulated by creating a "trampoline" (he gave
a code example by [James Tauber](https://twitter.com/#!/jtauber)) but I did not
quite understand how this works.  And it is very very slow, so not really an
option.

# Currying

Transforms a function that takes multiple arguments into a chain of unary
functions, which is the standard in Haskell.

# Conclusion

* Gavin says that learning functional programming can make you a better Python
  programmer.
* You have to know a lot of math like category theory and type theory
* You should play with different functional programming languages
* Structure and Interpretation of Computer Programs is a good book to
  understand functional programming.
