Date: 2013-07-01
Title: Rethinking Presentations 
Tagline: Why My Current Presentation Stack Needs an Overhaul
Slug: presentations
Category: Blog
Tags: presentations, thoughts

I'm currently preparing a long tutorial about [Linux essentials](https://docs.google.com/document/d/11VN5YN98WG53VHFAbzLuGNLyFw-iaNC78igHOJpjN5o/edit?usp=sharing).
While I really love Apple's Keynote and Github's [Speaker Deck](https://speakerdeck.com/mbrochh), 
I'm afraid  that for this undertaking my usual "presentation stack" is not 
going to cut it. Here is why:

### 1. Collaboration

I will team up with [Luther Goh Lu Feng](https://twitter.com/elfgoh). He is a 
well known Python developer at Hackerspace.SG and always looking for 
opportunities to spread the knowledge about all things digital.

We will be working on the slides remotely as a team, therefore 
Keynote is out of question. OK you could argue that we could just share the
working file on Dropbox but that is bound to cause tons of file conflicts.

Google Docs would be an option, but it is not the best one because Google's 
change history is not really helpful. First of all, it saves a million 
changes, secondly I would have to click at a change and then scroll through the
whole file in order to see what has been changed.

A solution based on Git would be better, because, you know, it is just the 
right tool for remotely collaborating on text-files.


### 2. Text Files

Text files? Oh yea! I really enjoy blogging with [Pelican](http://martinbrochhaus.com/pelican2.html).
Why? Because I don't need to be online (unlike Wordpress) in order to write my
posts. I can just open up Vim and start writing. No distractions, just me and
the words unfolding.

I want a presentation software that does not obfuscate my content in some
proprietary format. If you think about it: Once that goal is reached we would
probably just end up with human readable text files again, which means we could 
edit them using our favourite text editor.

And of course, when we are just dealing with text files, versioning them with
Git would be a natural thing to do. 


### 2. Colors

The tutorial will be very long and cover a huge amount of knowledge. I'm afraid
that some attendants might give up halfway thinking that they have learnt 
enough or wondering when this torture is going to end.

Therefore I want to give a brief overview of all topics at the
beginning and show why and how they relate to each other. I believe that giving 
color codes to each topic would be a good way to build a mental map inside the
attendant's heads and keep in mind how far we have gotten in the presentation
and what we are currently talking about.

Now check out [this slide](http://lab.hakim.se/reveal-js/#/12) and press 
`right arrow`. See how nicely the background color changes? Keynote or Google 
Docs are not built for this usecase. They force a theme upon me and want me to 
keep it for the whole talk. Boring!


### 3. Syntax highlighting

I recently gave a talk at PyCon Singapore about [writing reusable Django apps](https://speakerdeck.com/mbrochh/writing-publishing-and-maintaining-reusable-django-apps?slide=18)
and naturally the slides of my talk contained a lot of code snippets. I'm
probably doing it wrong but I painstakingly copied all those snippets into
text boxes, changed font, color, background, border and arranged them on the 
slide. And I don't even have syntax highlighting for them.

This sucks! I want a presentation software that is built for showing code.
Guess what: [Reveal.js highlights code](http://lab.hakim.se/reveal-js/#/12)
beautifully.


### 4. Cross device publishing

Speaker Deck looks quite decent on a mobile device but it's really not very 
responsive because it takes quite some time to load the whole presentation. 
Another problem is: You can't select the code snippets and copy and paste them. 
You would have to download the presentation as a PDF, which no one ever does.

Let's face it, most developers find content via social networks using their
smartphones, for example while they are commuting. If someone followed a link 
to one of my presentations using his smartphone I want him to be able to read 
my presentation regardless of his device.

I'm also not sure how well Google would index presentations hosted on Speaker 
Deck. With slides made of pure HTML this should be no issue.


### 5. Virtual classroom

At PyCon Singapore I also gave a tutorial about [hosting Django sites on Webfaction](https://speakerdeck.com/mbrochh/hosting-complex-web-applications-on-webfaction-servers).
It was supposed to be a hands on tutorial and I took countless hours to make 
sure that all code snippets work. However, after two hours we were still at
the most basic slides and I had to stop the hands-on session and rush through
the rest of the tutorial myself without waiting for the audience to catch up.

The problem was that the audience had to copy the commands via reading them 
from the projection screen and typing them in manually. I thought that this
would be no big deal but you would be amazed about all those subtle little 
typos people can come up with.

Therefore I want a presentation software which allows me to show the 
presentation on every attendant's screen. That way they could read everything 
clearly right in front of their eyes and they could even copy and paste the
commands during the hands-on exercises.


### Enter Reveal.js

Astoundingly, it took me just about 5 minutes of research to find a solution 
that solves all my problems single-handedly: Enter [Reveal.js](http://lab.hakim.se/reveal-js/).

* The presentation is just a HTML file. That's a text file.
* Therefore I can easily collaborate on it using Git
* I can use Markdown and syntax highlighting in my slides
* And I can work on it using my favorite text editor
* I can host it on Github and nicely display it on any device
* It allows me to easily change the background color of my slides
* I can use [multiplexing](https://github.com/hakimel/reveal.js#multiplexing)
  to allow my audience to follow the presentation on their own screens

I only found one drawback so far: Reveal.js needs to have the whole 
presentation in one big `index.html` file. This contradicts my need for
collaboration because once again, merge conflicts would become a major issue.

Luckily I quickly found a pretty cool solution around this and I also figured
out a nice way to host my presentation on Github.

How I did that? I will post a little how-to tomorrow. Stay tuned!
