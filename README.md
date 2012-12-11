# Landslide

Landslide generates a slideshow using from markdown, ReST, or textile. It
builds off of Google's [html5slides][html5slides] template.

The following markdown produces [this slideshow][sample].

    # Landslide

    ---

    # Overview

    Generate HTML5 slideshows from markdown, ReST, or textile.

    ![python](http://i.imgur.com/bc2xk.png)

    Landslide is primarily written in Python, but it's themes use:

    - HTML5
    - Javascript
    - CSS

    ---

    # Code Sample

    Landslide supports code snippets

        !python
        def log(self, message, level='notice'):
            if self.logger and not callable(self.logger):
                raise ValueError(u"Invalid logger set, must be a callable")

            if self.verbose and self.logger:
                self.logger(message, level)

[html5slides]: http://code.google.com/p/html5slides/
[sample]: http://adamzap.com/misc/presentation.html

# Requirements

`python` and the following modules:

- `jinja2`
- `pygments` for code blocks syntax coloration

### Markup Conversion

- `markdown` if you use Markdown syntax for your slide contents
- `docutils` if you use ReStructuredText syntax for your slide contents
- `textile` for textile support

### Optional

- `watchdog` for watching/auto-regeneration with the `-w` flag
- [PrinceXML](http://www.princexml.com/) for PDF export

# Installation

Install the latest stable version of Landslide with a python package manager
like `pip`:

    $ pip install landslide

If you want to stay on the edge:

    $ git clone https://github.com/adamzap/landslide.git
    $ cd landslide
    $ python setup.py build
    $ sudo python setup.py install

# Formatting

## Markdown

- Your Markdown source files must be suffixed by `.md`, `.markdn`, `.mdwn`,
  `.mdown` or `.markdown`
- To create a title slide, render a single `h1` element (eg. `# My Title`)
- Separate your slides with a horizontal rule (`---` in markdown) except at the
  end of md files
- Your other slides should have a heading that renders to an `h1` element
- To highlight blocks of code, put `!lang` where `lang` is the pygment
  supported language identifier as the first indented line

## ReStructuredText

- Your ReST source files must be suffixed by `.rst` or `.rest` (**`.txt` is not
  supported**)
- Use headings for slide titles
- Separate your slides using an horizontal rule (`----` in RST) except at the
  end of RST files

## Textile

- Textile cannot generate `<hr />`, so you must insert those manually to separate
  slides

# Rendering

- Run `landslide slides.md` or `landslide slides.rst`
- Enjoy your newly generated `presentation.html`

Or get it as a PDF document if PrinceXML is installed and available on your
system:

    $ landslide README.md -d readme.pdf
    $ open readme.pdf

# Viewing

- Press `h` to toggle display of help
- Press `left arrow` and `right arrow` to navigate
- Press `t` to toggle a table of contents for your presentation. Slide titles
  are links
- Press `ESC` to display the presentation overview (Exposé)
- Press `n` to toggle slide number visibility
- Press `b` to toggle screen blanking
- Press `c` to toggle current slide context (previous and next slides)
- Press `e` to make slides filling the whole available space within the
  document body
- Press `S` to toggle display of link to the source file for each slide
- Press '2' to toggle notes in your slides (specify with the .notes macro)
- Press '3' to toggle pseudo-3D display (experimental)
- Browser zooming is supported

# Commandline Options

Several options are available using the command line:

    -h, --help            show this help message and exit
    -c, --copy-theme      Copy theme directory into current presentation source
                          directory
    -b, --debug           Will display any exception trace to stdin
    -d FILE, --destination=FILE
                          The path to the to the destination file: .html or .pdf
                          extensions allowed (default: presentation.html)
    -e ENCODING, --encoding=ENCODING
                          The encoding of your files (defaults to utf8)
    -i, --embed           Embed stylesheet and javascript contents,
                          base64-encoded images in presentation to make a
                          standalone document
    -l LINENOS, --linenos=LINENOS
                          How to output linenos in source code. Three options
                          availables: no (no line numbers); inline (inside <pre>
                          tag); table (lines numbers in another cell, copy-paste
                          friendly)
    -o, --direct-output    Prints the generated HTML code to stdin; won't work
                          with PDF export
    -q, --quiet           Won't write anything to stdin (silent mode)
    -r, --relative        Make your presentation asset links relative to current
                          pwd; This may be useful if you intend to publish your
                          html presentation online.
    -t THEME, --theme=THEME
                          A theme name, or path to a landlside theme directory
    -v, --verbose         Write informational messages to stdin (enabled by
                          default)
    -w, --watch           Watch the source directory for changes and
                          auto-regenerate the presentation
    -x EXTENSIONS, --extensions=EXTENSIONS
                          Comma-separated list of extensions for Markdown

# Presentation Configuration

Landslide allows to configure your presentation using a `cfg` configuration
file, therefore easing the aggregation of source directories and the reuse of
them across presentations. Landslide configuration files use the `cfg` syntax.
If you know `ini` files, you get the picture. Below is a sample configuration
file:

    [landslide]
    theme  = /path/to/my/beautiful/theme
    source = 0_my_first_slides.md
             a_directory
             another_directory
             now_a_slide.markdown
             another_one.rst
    destination = myWonderfulPresentation.html
    css =    my_first_stylesheet.css
             my_other_stylesheet.css
    js =     jquery.js
             my_fancy_javascript.js
    relative = True
    linenos = inline

Don't forget to declare the `[landslide]` section.  All configuration files
must end in the .cfg extension.

To generate the presentation as configured, just run:

    $ cd /path/to/my/presentation/sources
    $ landslide config.cfg

# Macros

You can use macros to enhance your presentation:

## Notes

Add notes to your slides using the `.notes:` keyword, eg.:

    # My Slide Title

    .notes: These are my notes, hidden by default

    My visible content goes here

You can toggle display of notes by pressing the `2` key.

Some other macros are also available by default: `.fx: foo bar` will add the
`foo` and `bar` classes to the corresponding slide `<div>` element, easing
styling of your presentation using CSS.

# Presenter Notes

You can also add presenter notes to each slide by following the slide content
with a heading entitled "Presenter Notes". Press the 'p' key to open the
presenter view.

# Registering Macros

Macros are used to transform the HTML contents of your slide.

You can register your own macros by creating `landslide.macro.Macro` derived
classes, implementing a `process(content, source=None)` method and returning
a tuple containing the modified contents and some css classes you may be
wanting to add to your slide `<div>` element. For example:

    !python
    import landslide

    class MyMacro(landslide.Macro):
      def process(self, content, source=None):
        return content + '<p>plop</p>', ['plopped_slide']

    g = landslide.generator.Generator(source='toto.md')
    g.register_macro(MyMacro)
    print g.render()

This will render any slide as below:

    !html
    <div class="slide plopped_slide">
      <header><h2>foo</h2></header>
      <section>
        <p>my slide contents</p>
        <p>plop</p>
      </section>
    </div>

# Advanced Usage

## Setting Custom Destination File

    $ landslide slides.md -d ~/MyPresentations/presentation.html

## Working with Directories

    $ landslide slides/

## Working with Direct Output

    $ landslide slides.md -o | tidy

## Using an Alternate Landslide Theme

    $ landslide slides.md -t mytheme
    $ landslide slides.md -t /path/to/theme/dir

## Embedding Base-64-Encoded Images

    $ landslide slides.md -i

## Exporting to PDF

    $ landslide slides.md -d presentation.pdf

# Theming

A Landslide theme is a directory following this simple structure:

    mytheme/
    |-- base.html
    |-- css
    |   |-- print.css
    |   `-- screen.css
    `-- js
        `-- slides.js

If a theme does not provide HTML and JS files, those from the default theme
will be used. CSS is not optional.

Last, you can also copy the whole theme directory to your presentation one by
passing the `--copy-theme` option to the `landslide` command:

    $ landslide slides.md -t /path/to/some/theme --copy-theme

# User stylesheets and Javascripts

If you don't want to bother making your own theme, you can include your own
user css and js files to the generated presentation.

This feature is only available if you use a landslide configuration file, by
setting the `css` and/or `js` flags:

    [landslide]
    theme  = /path/to/my/beautiful/theme
    source = slides.mdown
    css =    custom.css
    js =     jquery.js
             powerpoint.js

These will link the ``custom.css`` stylesheet and both the ``jquery.js`` and
``powerpoint.js`` files within the ``<head>`` section of the presentation html
file.

**NOTE:** Paths to the css and js files must be relative to the directory
you're running the ``landslide`` command from.

# Publishing your Presentation Online

If you intend to publish your HTML presentation online, you'll have to use the
`--relative` option, as well as the `--copy-theme` one to have all asset links
relative to the root of your presentation;

    $ landslide slides.md --relative --copy-theme

That way, you'll just have to host the whole presentation directory to
a webserver. Of course, no Python nor PHP nor anything else than a HTTP
webserver (like Apache) is required to host a landslide presentation.

[Here's an example][akei-pres].

[akei-pres]: http://www.akei.com/presentations/2011-Djangocong/index.html

# Theme Variables

The `base.html` must be a [Jinja2 template file][jinja-docs] where you can
harness the following template variables:

- `css`: the stylesheet contents, available via two keys, `print` and `screen`,
  both having:
  - a `path_url` key storing the url to the asset file path
  - a `contents` key storing the asset contents
- `js`: the javascript contents, having:
  - a `path_url` key storing the url to the asset file path
  - a `contents` key storing the asset contents
- `slides`: the slides list, each one having these properties:
  - `header`: the slide title
  - `content`: the slide contents
  - `number`: the slide number
- `embed`: is the current document a standalone one?
- `num_slides`: the number of slides in current presentation
- `toc`: the Table of Contents, listing sections of the document. Each section
  has these properties available:
  - `title`: the section title
  - `number`: the slide number of the section
  - `sub`: subsections, if any

[jinja-docs]: http://jinja.pocoo.org/2/documentation/templates

# Styles Scope

- To change HTML5 presentation styles, tweak the `css/screen.css` stylesheet
  bundled with the theme you are using
- For PDF, modify the `css/print.css`

# Authors

## Original Author and Development Lead

- Adam Zapletal (adamzap@gmail.com)

## Co-Author

- Nicolas Perriault (nperriault@gmail.com)

## Contributors

See https://github.com/adamzap/landslide/contributors

## Base Template Authors and Contributors (html5-slides)

- Marcin Wichary (mwichary@google.com)
- Ernest Delgado (ernestd@google.com)
- Alex Russell (slightlyoff@chromium.org)
