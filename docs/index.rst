Landslide's documentation
=========================

Landslide_ is a command-line based presentation generator relying on Web standards (html, javascript, css) and some Python_ libraries such as Jinja2_, Pygments_, docutils_ and Markdown_.

Installation
------------

Landslide requires Python_ v2.5 minimum and these dependencies installed:

* The Jinja2_ template engine
* Pygments_ for code syntax highlighting

One of the syntax handlers above:

* The Markdown_ python library if you intend to write your slides contents using the Markdown_ syntax
* or the docutils_ package if you rather prefer using reStructuredText_.

The easiest way to install Landslide_ is using Pip_::

    $ pip install landslide

Alternatively, you can use easy_install_::

    $ easy_install landslide

If you rather want to stay `on the edge`_::

    $ git clone https://github.com/n1k0/landslide.git
    $ cd landslide
    $ python setup.py build
    $ sudo python setup.py install

Basic Usage
-----------

Using the Markdown_ syntax
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Your Markdown source files must be suffixed by ``.md``, ``.markdn``, ``.mdown`` or ``.markdown``
* To create a title slide, render a single h1 element (eg. ``# My Title``)
* Separate your slides with a horizontal rule (``---`` in markdown) except at the end of markdown files
* Your other slides should have a heading that renders to an ``<h1>`` or ``<h2>`` element
* To highlight blocks of code, put ``!{lang}`` where ``{lang}`` is the pygment supported language identifier as the first indented line

Here's a sample presentation based on Markdown::

    # My Presentation Heading
    ---
    ## My First Slide Title
    With some contents
    ---
    ## My Second Slide Title
    With some contents

Using the reStructuredText_ syntax
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bar

API Documentation
-----------------

Generator
~~~~~~~~~

.. automodule:: landslide.generator
    :members:

Macros
~~~~~~

.. automodule:: landslide.macro
    :members:

Parser
~~~~~~

.. automodule:: landslide.parser
    :members:

Utils
~~~~~

.. automodule:: landslide.utils
    :members:

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. links

.. _docutils: http://docutils.sourceforge.net/
.. _easy_install: http://packages.python.org/distribute/easy_install.html
.. _Jinja2: http://jinja.pocoo.org/
.. _Landslide: https://github.com/n1k0/landslide
.. _Markdown: http://daringfireball.net/projects/markdown/
.. _on the edge: https://github.com/n1k0/landslide/commits/master/
.. _Pip: http://pip.openplans.org/
.. _Pygments: http://pygments.org/
.. _Python: http://python.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html