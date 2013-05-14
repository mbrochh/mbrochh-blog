Date: 2012-06-07
Title: PyCon APAC 2012 - Introduction to Game Development
Slug: pygame
Category: Blog
Tags: python, pycon, conferences

I like how [Daniel Greenfeld](https://twitter.com/pydanny) has the habit of
publishing [live notes](http://pydanny-event-notes.readthedocs.org/en/latest/index.html)
when he attends conferences and meet-ups. I don't think that I will have the
time and money to attend so many conferences that a dedicated repository would
make sense but I guess that I can give this a try right here in my blog.

So here are my notes on [Richard Jone's](https://plus.google.com/100267502615190755251/posts)
tutorial on game development with Python:

We got a .zip file with a whole game inside. Richard was nice enough to put it
into public domain, so we can tinker with it and build upon it.

# Display Something

* We can display images, draw primitives, draw fonts or use OpenGL.
* Not going to cover OpenGL today, unfortunately.

A first pygame program is really simple:

    ::py
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))


Better put some structure to your code. Create a Game() class with a main()
method. Don't use global variables.

In pygame, unlike in modern frameworks, the coordinate ``0,0`` is the top left
corner. This is because video hardware draws like this. More modern systems
like OpenGL separate the drawing part from the display part so that we can use
a more sane coordinate system with ``0,0`` at bottom left. Pygame is not that
modern unfortunately.

Let's draw something:

    ::py
    image = pygame.image.load('player.png')
    screen.fill((200, 200, 200))  # Fill the screen with a background color
    screen.blit(image, (320, 240))  # Copies the image to that position on screen
    pygame.display.flip()

Pygame uses RGB colors.

We learn about "tearing". If we draw to the screen directly, the screen might
refresh while we change what is on the screen so we will see something in
between. Therefore we will write to a second screen buffer first and once we
are done drawing everything we will `flip` the buffers so that the display will
re-draw the now new buffer. I assume that the ``display.flip()`` method does
somehow know when the display finished drawing one whole screen and will only
flip once that is done.

Via ``pygame.tick.Clock()`` we can put the main loop to sleep. No need to
stress our CPU like crazy. 30 FPS should be a good frame rate for any video
game.

Our first animation is just adding 10 pixels to the image position.

# User input

While Pygame can tell us, if a key down event has recently happened, it can
also tell us which keys are currently being pressed:

    ::py
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        image_x -= 10

Both can be useful. Since the main loop runs with a clock and goes to sleep
every 30 seconds, it can very well happen that the user pressed the escape key
to quit the game while we have been sleeping. In this case we would check like
this:

    ::py
    event = pygame.event.get()
    if event.type == pygame.KEYDOWN and event.key = pygame.K_ESCAPE:

# Sprites

To put things together, we can define sprites, which are images, that know how
they look like and where they are on screen. We can give them an ``update``
method and handle their user input, which pulls out a lot of clutter from our
main loop:

    ::py
    class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('player.png')
        self.rect = pygame.rect.Rect((320, 240), self.image.get_size())

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 10

You would want to pass the amount of time that has passed since the last loop
call and pass it into the update method. Then don't just jump 10 pixels but
multiply the passed time with a value. This will make the game feel more smooth
and more equal on different hardware.

# Collision detection

Axis-Aligned bounding box is the most common collision detection. The name says
it all, think about it.

An alternative would be to use circles as bounding boxes.

A third alternatives is to use a hash map, which is useful for 2D games with
thousands of sprite on screen. This is usually used for so called [Bullet
Hell](https://en.wikipedia.org/wiki/Bullet_hell#Bullet_hell) games. Didn't know
about this term before. I'm feeling ashamed.

You could finally do pixel perfect collision detection but that might be quite
slow. It would be used in games like Worms, where you can blow up the whole
environment, which results in shapes that cannot be handled by bounding boxes
any more.

# Tile maps

.tmx is a common format for tile maps that make up the game world.  It has an
editor called [Tiled](http://mapeditor.org). You can kind of paint the map of
that level. The tile map also has a layer of trigger tiles which are invisible
but can be accessed by the game program. Therefore, thanks to the .tmx
standard, the game can know about the position, the look and the type (trigger)
of any tile of the game world.

The player only sees a fraction of the whole tile map. This is called the view
port.

From here on it is pretty much all about doing lots of if and else clauses
reacting to collisions and inputs. It seems to me that the hardest part about
game development is structuring your code as efficient as possible because it
can quickly grow into a huge amount of spaghetti code.

# Sound

As expected, adding sound is extremely easy as well:

    ::py
    self.jump = pygame.mixer.Sound('jump.wav')
    self.jump.play()

[SFXR](https://code.google.com/p/sfxr/) is a great little tool that emulates
the sound chip of the C64 and allows you to model cute 8bit sounds for your
game.

# Special effects

You can use ``pip install lepton``, a library for particles. Richard repeats:
"Every single game improves with particles" :) He mentions a talk called
[Juice it or lose it](https://www.youtube.com/watch?v=Fy0aCDmgnxg) which is
about techniques to juice up your game with special effects.

# Where to go from here

* [pygame.org](http://pygame.org)
* [inventwithpython](http://inventwithpython.com)
* [pyweek.org](http://pyweek.org)

# Tools

* [mapeditor.org](http://mapeditor.org) - Creates tile maps
* [SFXR](https://code.google.com/p/sfxr/) - Creates sound files
* [Pyxel Edit](http://danikgames.com/stuff/pyxeledit/) - Creates seamless
  tiles.
* [Pixen](http://pixenapp.com/) - Creates moving animatinos for characters
* [cocos2d.org](http://cocos2d.org/doc.html) - Helps with adding juice
* [py2exe](http://www.py2exe.org/) - Bundle your game and distribute it as an
  .exe file
* [py2app](http://svn.pythonmac.org/py2app) - Bundle your game and distribute
  as an OSX application

# Conclusion

It is _amazingly_ simple to start with game development and Python. Everything
form installing pygame to getting to play a first prototype just works and
there seem to be free tools available for every aspect of simple game
development (like creating sound etc.). I definitely want to try this at home!
This might be the most awesome way to teach my 12 year old brother in law about
programming.
