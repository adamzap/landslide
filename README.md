html5-slides-markdown
=====================

Generates a slideshow using the slides that power
[the html5-slides presentation](http://apirocks.com/html5/html5.html).

A sample slideshow is [here](http://adamzap.com/random/html5-slides-markdown.html).

A `python` with the `jinja2`, `markdown`, and `pygments` modules is required.

Markdown Formatting Instructions
--------------------------------

- Separate your slides with a horizontal rule (--- in markdown)
- Your first slide (title slide) should not have a heading, only `<p>`s
- Your other slides should have a heading that renders to an h1 element
- To highlight blocks of code, put !{{lang}} as the first indented line
- See the included slides.md for an example

Rendering Instructions
----------------------

- Put your markdown content in a file called `slides.md`
- Run `python render.py` (or `./render.py`)
- Enjoy your newly generated `presentation.html`

Options
-------

Several options are available using the command line:

    $ ./render.py --help
    Usage: render.py [options]

    Options:
      -h, --help            show this help message and exit
      -s FILE, --source=FILE
                            The path to the markdown source file
      -d FILE, --destination=FILE
                            The path to the to the destination
      -t FILE, --template=FILE
                            The path to the to the Jinja2 template file
      -e ENCODING, --encoding=ENCODING
                            The encoding of your files (defaults to utf8)

TODO
----

- Test CSS for all Markdown features

Thanks
------

- bradcupit (for suggestions and encouragement)
