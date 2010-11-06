Slides in ReStructuredText
==========================

----

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

Middle Title Slide
==================

----

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

Let me give you this snippet::

    !python
    def foo():
        "just a test"
        print bar

Then this one, a more ReSTful way (haha, nerd joke spotted)::

.. sourcecode:: python

    def foo():
        "just a test"
        print bar

Or as an alternative::

.. code-block:: python

    def foo():
        "just a test"
        print bar
