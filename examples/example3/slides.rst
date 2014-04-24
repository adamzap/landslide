Slides in ReStructuredText
==========================

Here we Go
----------

This is foo

This is bar

This is ünicô∂e

- This
- Is
- A
- List

----

My Slides
=========

My First
--------

I want an image here:

.. image:: monkey.jpg

----

My Second
---------

I want a video here:

.. video:: test.webm

----

My Third
--------

I want audio here:

.. audio:: test.ogg

----

My Fourth
---------

I want a youtube video here:

.. youtube:: H9kXPTwIO08

----


Middle Title Slide
==================

Here we Go Again
----------------

This is foo again

This is bargain

----

RST Features
------------

*italics*

**bold**

``monospace``

http://docutils.sf.net/

1. one
2. two

----

Some code now
-------------

Let me give you this snippet:

.. sourcecode:: python

    def foo():
        "just a test"
        print bar

Then this one, a more ReSTful way (haha, nerd joke spotted) using the ``sourcecode`` directive:

.. sourcecode:: python

    def bar():
        """pretty cool"""
        print baz


Then this other one with the ``code-block`` directive:

.. code-block:: python

    def batman():
        "foobar"
        return robin

