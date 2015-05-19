#!/usr/bin/env python

# TODO: Reword some of these and/or make them shorter
'''
Usage: landslide [options] <source-or-config-file> [<source-files>...]

--version           Show version number and exit
-h, --help          Show this help message and exit
-c, --copy-theme    Copy theme directory into presentation source directory
-b, --debug         Display exception tracebacks
-d FILE, --destination=FILE
                    Destination file for slideshow, default is presentation.html
-e ENCODING, --encoding=ENCODING
                    The encoding of your files (defaults to utf8)
-i, --embed         Embed all CSS, JS, and images into output file
-l LINENOS, --linenos=LINENOS
                    How to output linenos in source code. Three options
                    availables: no (no line numbers); inline (inside <pre>
                    tag); table (lines numbers in another cell, copy-paste
                    friendly)
-o, --direct-output
                    Print the generated HTML code to stdout; won't work with
                    PDF export
-P, --no-presenter-notes
                    Don't include presenter notes in the output
-q, --quiet         Don't write anything to stdout
-r, --relative      Make your presentation asset links relative to the current
                    directory; This may be useful if you intend to publish your
                    html presentation online.
-t THEME, --theme=THEME
                    A theme name or path to a landlside theme directory
-x EXTENSIONS, --extensions=EXTENSIONS
                    Comma-separated list of extensions for Markdown
-w, --watch         Watch source directory for changes and regenerate slides
-m, --math-output   Enable mathematical output using MathJax
'''

from docopt import docopt

# TODO: There must be a better way
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from options import Options
from presentation import Presentation


def main(argv=None):
    arguments = docopt(__doc__, argv, version='Landslide v2.0.0')

    options = Options(arguments)

    Presentation(options)


if __name__ == '__main__':
    main()
