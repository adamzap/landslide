html5-slides-markdown
=====================

Generates a slideshow using the slides that power
[the html5-slides presentation](http://apirocks.com/html5/html5.html).

A sample slideshow is [here](http://adamzap.com/random/html5-slides-markdown.html).

News
----

**06/11/10** - Current slideshows will need to be updated. As of tonight's changes
(48024cfe), title slides are rendered like any other. This means that you must
render them to an h1 element (# or = below). This is cleaner and more
consistent.

Requirements
------------

`python` and the following modules:

- `jinja2`
- `markdown`
- `pygments`

Markdown Formatting Instructions
--------------------------------

- To create a title slide, render a single h1 element
- Separate your slides with a horizontal rule (`---` in markdown)
- Your other slides should have a heading that renders to an h1 element
- To highlight blocks of code, put `!{{lang}}` where `{{lang}}` is the pygment supported language identifier as the first indented line
- See the included `slides.md` for an example

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
      -d FILE, --destination=FILE
                            The path to the to the destination
      -e ENCODING, --encoding=ENCODING
                            The encoding of your files (defaults to utf8)
      -t FILE, --template=FILE
                            The path to the to the Jinja2 template file
      -o, --direct-ouput    Prints the generated HTML code to stdin
      -q, --quiet           Won't write anything to stdin
      -s FILE, --source=FILE
                            The path to the markdown source file, or a directory
                            containing several files to combine
      -v, --verbose         Write informational messages to stdin (enabled by
                            default)

Advanced Usage
--------------

### Setting Cutom Destination File

    $ ./render.py -d ~/MyPresentations/KeynoteKiller.html

### Working with Directories

    $ ./render.py -s slides/

### Working with Direct Output

    $ ./render.py -o |tidy

### Using and Alternate Jinja2 Template

    $ ./render.py -t ~/templates/mytemplate.html

TODO
----

- Test CSS for all Markdown features

Authors
-------

- Adam Zapletal ([adamzap](http://github.com/adamzap))
- Brad Cupit ([bradcupit](github.com/bradcupit))
- Nicolas Perriault ([n1k0](github.com/n1k0))
- Vincent Agnano ([vinyll](github.com/vinyll))
