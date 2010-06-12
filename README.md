html5-slides-markdown
=====================

Generates a slideshow using the slides that power
[the html5-slides presentation](http://apirocks.com/html5/html5.html).

![demo](http://files.droplr.com.s3.amazonaws.com/files/6619162/1bcGcm.html5_presentation.png)

A sample slideshow is [here](http://adamzap.com/random/html5-slides-markdown.html).

---

News
----

**06/11/10** - Current slideshows will need to be updated. As of tonight's changes
(48024cfe), title slides are rendered like any other. This means that you must
render them to an h1 element (# or = below). This is cleaner and more
consistent.

---

Features
--------

- Write your slide contents easily using the [Markdown syntax](http://daringfireball.net/projects/markdown/syntax)
- HTML5, Web based, stand-alone document, fancy transitions
- PDF export (using [PrinceXML](http://www.princexml.com/) if available)

---

Requirements
------------

`python` and the following modules:

- `jinja2`
- `markdown`
- `pygments`

---

Markdown Formatting Instructions
--------------------------------

- To create a title slide, render a single h1 element
- Separate your slides with a horizontal rule (`---` in markdown)
- Your other slides should have a heading that renders to an h1 element
- To highlight blocks of code, put !`{lang}` where `{lang}` is the pygment supported language identifier as the first indented line
- See the included `slides.md` for an example

---

Rendering Instructions
----------------------

- Put your markdown content in a file called `slides.md`
- Run `python render.py` (or `./render.py`)
- Enjoy your newly generated `presentation.html`

As a proof of concept, you can even transform this annoying README into a fancy presentation:

    $ ./render.py -s README.md && open presentation.html

Or get it as a PDF document, at least if PrinceXML is installed and available on your system:

    $ ./render.py -s README.md -d readme.pdf && open readme.pdf

---

Options
-------

Several options are available using the command line:

    $ ./render.py 
    Adding slides.md
    Generated file: presentation.html
    ~/Sites/html5-slides-markdown $ ./render.py --help
    Usage: render.py [options]

    Options:
      -h, --help            show this help message and exit
      -d FILE, --destination=FILE
                            The path to the to the destination file: .html or .pdf
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

---

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

### Exporting to PDF

    $ ./render.py -s MySlides.md -d PowerpointIsDead.pdf

---

TODO
----

- Test CSS for all Markdown features
- Get rid of the annoying princexml warnings on PDF generation (princexml can't handle html5 tags like `<header>` but generated PDFs are okay)

---

Authors
-------

- Adam Zapletal ([adamzap](http://github.com/adamzap))
- Brad Cupit ([bradcupit](github.com/bradcupit))
- Nicolas Perriault ([n1k0](github.com/n1k0))
- Vincent Agnano ([vinyll](github.com/vinyll))
