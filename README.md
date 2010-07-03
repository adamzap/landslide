Landslide
=========

---

Overview
========

Generates a slideshow using the slides that power
[the html5-slides presentation](http://apirocks.com/html5/html5.html).

![demo](http://files.droplr.com.s3.amazonaws.com/files/6619162/1bcGcm.html5_presentation.png)

A sample slideshow is [here](http://adamzap.com/random/landslide.html).

---

News
====

07/03/10
--------

- Themes have landed. A Landslide theme is a directory having a `base.html` Jinja2 templates and optionnaly stylesheets and javascript. Have a look at the dedicated section in the present document. Please note that the `-t` option doesn't reference a template filepath anymore, but rather a theme name or path.
- A Table of Contents is now generated and available by hitting the `t` key (styles will be enhanced later)
- Slide numbers are now displayed

06/24/10
--------

- Version 0.4.0 is tagged, and Landslide is on [pypi](http://pypi.python.org/pypi/landslide/0.4.0).
- Landslide installs as a command line script if you install it via `easy_install` or `pip`.

---

Features
========

- Write your slide contents easily using the [Markdown syntax](http://daringfireball.net/projects/markdown/syntax)
- HTML5, Web based, stand-alone document (embedded local images), fancy transitions
- PDF export (using [PrinceXML](http://www.princexml.com/) if available)

---

Requirements
============

`python` and the following modules:

- `jinja2`
- `markdown`
- `pygments`

---

Markdown Formatting Instructions
================================

- To create a title slide, render a single `h1` element (eg. `# My Title`)
- Separate your slides with a horizontal rule (`---` in markdown)
- Your other slides should have a heading that renders to an `h1` element
- To highlight blocks of code, put !`{lang}` where `{lang}` is the pygment supported language identifier as the first indented line
- See the included `slides.md` for an example

---

Rendering Instructions
======================

- Put your markdown content in a Markdown file, eg `slides.md`
- Run `landslide slides.md`
- Enjoy your newly generated `presentation.html`

As a proof of concept, you can even transform this annoying `README` into a fancy presentation:

    $ landslide README.md && open presentation.html

Or get it as a PDF document, at least if PrinceXML is installed and available on your system:

    $ landslide README.md -d readme.pdf
    $ open readme.pdf

---

Options
=======

Several options are available using the command line:

    $ landslide/landslide 
    Usage: landslide [options] input.md ...

    Generates fancy HTML5 or PDF slideshows from Markdown sources

    Options:
      -h, --help            show this help message and exit
      -b, --debug           Will display any exception trace to stdin
      -d FILE, --destination=FILE
                            The path to the to the destination file: .html or .pdf
                            extensions allowed (default: presentation.html)
      -e ENCODING, --encoding=ENCODING
                            The encoding of your files (defaults to utf8)
      -i, --embed           Embed base64-encoded images in presentation
      -t THEME, --theme=THEME
                            A theme name, or path to a landlside theme directory
      -o, --direct-ouput    Prints the generated HTML code to stdin; won't work
                            with PDF export
      -q, --quiet           Won't write anything to stdin (silent mode)
      -v, --verbose         Write informational messages to stdin (enabled by
                            default)

    Note: PDF export requires the `prince` program: http://princexml.com/

---

Advanced Usage
==============

### Setting Custom Destination File

    $ landslide slides.md -d ~/MyPresentations/KeynoteKiller.html

### Working with Directories

    $ landslide slides/

### Working with Direct Output

    $ landslide slides.md -o | tidy

### Using an Alternate Landslide Theme

    $ landslide slides.md -t mytheme
    $ landslide slides.md -t /path/to/theme/dir

### Embedding Base-64-Encoded Images

    $ landslide slides.md -i

### Exporting to PDF

    $ landslide slides.md -d PowerpointIsDead.pdf

---

Theming
=======

A Landlside theme is a directory following this simple structure:

    mytheme/
    |-- base.html
    |-- css
    |   |-- print.css
    |   `-- screen.css
    `-- js
        `-- slides.js

The `base.html` must be a [Jinja2 template file](http://jinja.pocoo.org/2/documentation/templates) where you can harness the following template variables:

- `css`: the stylesheet contents, available via two keys: `print` and `screen`
- `js`: the javascript contents
- `slides`: the slides list, each one having these properties:
  - `header`: the slide title
  - `content`: the slide contents
  - `number`: the slide number
- `num_slides`: the number of slides in current presentation
- `toc`: the Table of Contents, listing sections of the document. Each section has these properties available:
  - `title`: the section title
  - `number`: the slide number of the section
  - `sub`: subsections, if any

TODO(?)
=======

- Abstract use of Markdown syntax and allow use of RST, Textile, etc.
- Manage presentation *projects*, each one having its own configuration file; the configuration file could configure:
    - theme (template, assets, etc)
    - sources to order and aggregate
    - destination
    - options
- Handle the case of markdown files aggregation, atm its necessary to write a `---` separator at the end of each one but the last

---

Authors
=======

See `AUTHORS.md`
