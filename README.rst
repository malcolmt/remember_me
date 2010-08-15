========
Minerva
========

Introduction and Basic Usage
=============================

Minerva is a foreign language vocabulary drill program. Primarily designed for
English speakers learning Asian languages. The initial implementation includes
Simplified Chinese and Japanese vocabulary, although none of the code is
specific to those two choices.

It was written as part of the `2010 Django Dash`_.

Users can either be registered or anonymous. Registered users can have their
progress tracked over multiple sessions. Participating as an anonymous user and
then registering results in progress for that session being retained as well.

The learning method is simple repetition. You are shown either an Engish
meaning or a foreign word and then a choice of options in the other language.
Select the correct option to match the word(s) in the question. New characters
are introduced in the normal flow of questions, so you might see a character
you don't know what it means yet. Pay attention to the correct answer and it
will be familiar the next time it comes around.

.. note:: Question selection

    The question selection algorithm is very rudimentary in this initial
    version. It's an are of almost limitless possibilities and the system
    design allows for experimentation there. Right now, words are graded by
    difficulty and easier words are presented first.

.. _2010 Django Dash: http://djangodash.com/

Installation
=============

Minerva is a couple of small Django applications with only a small number of
external pre-requisites. The simplest way to get up and running quickly is
using our script to create a virtualenv_ environment. Assuming you already have
virtualenv and pip_ installed, run the ``create.sh`` shell script in the
``scripts/`` directory, passing it the location of the virtual environment::

    scripts/create.sh ~/little_web_app_that_could

Then link in the current source code and activate the virtualenv::

    cd ~/little_web_app_that_could
    ln -s <remember_me location> remember_me
    . bin/activate

The default setup uses a local SQLite database and all the data for Chinese and
Japanese training is included. However, you need to create the initial database
and populate the data. Continuing on from the above::

    cd remember_me
    python manage.py syncdb

    # (Answer questions as prompted...)

    python manage.py migrate

    # (Wait a couple of minutes...)

    python manage.py runserver

    # (Visit http://localhost:8000/...)
    # (Have a rewarding beverage of choice)

.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _pip: http://pypi.python.org/pypi/pip

Manual setup
-------------

For those wanting to know what's going on in the setup phase, the requirements
for this set of apps are

    * Django 1.2.1
    * django-south
    * django-debug-toolbar
    * BeautifulSoup (if recreating the Japanese vocab data)

If you already have those installed, there's nothing else that needs to be done.

TODO
=====

Obviously for something initially developed with about 20 hours of work spread
over a couple of days, there are a lot of possibilities that we haven't had
time to implement. These are noted here for our own future development efforts
and in case people are interested.

Registration
-------------

It should be relatively straightforward to hook up with something like
django-socialregistration to allow signing up via Facebook or Twitter or
external registration system of choice. Not sure that socialregistration is
necessarily the right choice here, but it's the type of thing we can use.

Question selection algorithm
-----------------------------

Things to consider
 - a new user with no state, what questions are provided to him/her
 - a user with no current session, would their progress be based on their progress record or current session

Information required
 - flag a word as being studied in the current session
 - number of times successfully studied in the current session
 - word weight

Basic algorithm
 - user submits answer
 - system analyses the result and adjusts the weight
 - new words may be selected if number of words is below a threshold

Result analysis
 - if answer is wrong
     - push down the weight of the one they got wrong and of the word they selected
 - if answer is right
     - push up the weight of the one they got right and increment times studied
     - if number of times successfully studied is over a threshold
          - Remove it from the studied item list

New word selection
 - select word with lowest attempt value

To Consider
 - retire old state

