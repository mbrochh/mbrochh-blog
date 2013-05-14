Date: 2012-06-08
Title: PyCon APAC 2012 - Analyzing Big Data in the Cloud
Slug: big-data-cloud
Category: Blog
Tags: python, pycon, conferences

Here are my notes on [Chris Boesch's](https://plus.google.com/110893970871115341770/about)
talk about analyzing big data in the cloud.

_Edit_: Here is the video: https://www.youtube.com/watch?v=ADjIt6ZbqKU

Chris is a professor teaching many IT subjects at Singapore Management
University.  He advertises the cool idea to let the students teach themselves
at their own pace. He will be there to answer questions but he says no one ever
comes back to him. Once thrown into the cold water, people just want to figure
it out themselves.

He developed [Singpath](http://www.singpath.com/eli/index.html), a playful
approach on learning Python online via a web powered tournament system. It runs
on Python on Google App Engine.

He asks his students to develop games and put them on Google App Engine. Then
he asks each team to play against the games of all other teams. A big
spreadsheet will show which group manages to beat which other group's game
which tuns out to be a great motivation for students to try harder and
implement their game more thoroughly. With Tic Tac Toe, where every game should
actually be a tie and the computer should never lose, this can be done nicely.
When students see that other groups are beating their Tic Tac Toe, that is
motivation enough to dive back into code and improve the AI.

He also uses [Coderbuddy](https://www.coderbuddy.com/), a service that helps
to deploy and test websites on Google App Engine.

# Agile is different

Chris discovered that when teaching people how to program using the cloud,
some of them instinctively start working extremely agile. This raises
interesting problems because you need teach a whole new bunch of topics like
unit testing or split testing. For Google App Engine there are some tools for
this:

* [gaeunit](https://code.google.com/p/gaeunit/)
* [gae-bingo](https://github.com/kamens/gae_bingo)

Uploading and downloading massive amounts of data into Google App Engine is
simple, can be done with a few dozen lines of code.

* [The Lean Startup](http://www.amazon.com/The-Lean-Startup-Entrepreneurs-Continuous/dp/0307887898?tag=duckduckgo-d-20)
