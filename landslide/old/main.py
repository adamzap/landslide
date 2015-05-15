#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from optparse import OptionParser

from . import generator
from . import __version__


def _parse_options():
    """Parses landslide's command line options"""

    parser = OptionParser(
        usage="%prog [options] input.md ...",
        description="Generates an HTML5 or PDF "
                    "slideshow from Markdown or other formats",
        epilog="Note: PDF export requires the `prince` program: "
               "http://princexml.com/",
        version="%prog " + __version__)

    parser.add_option(
        "-c", "--copy-theme",
        action="store_true",
        dest="copy_theme",
        help="Copy theme directory into current presentation source directory",
        default=False)

    parser.add_option(
        "-b", "--debug",
        action="store_true",
        dest="debug",
        help="Will display any exception trace to stdout",
        default=False)

    parser.add_option(
        "-d", "--destination",
        dest="destination_file",
        help="The path to the to the destination file: .html or "
             ".pdf extensions allowed (default: presentation.html)",
        metavar="FILE",
        default="presentation.html")

    parser.add_option(
        "-e", "--encoding",
        dest="encoding",
        help="The encoding of your files (defaults to utf8)",
        metavar="ENCODING",
        default="utf8")

    parser.add_option(
        "-i", "--embed",
        action="store_true",
        dest="embed",
        help="Embed stylesheet and javascript contents, "
             "base64-encoded images in presentation to make a "
             "standalone document",
        default=False)

    parser.add_option(
        "-l", "--linenos",
        type="choice",
        choices=generator.VALID_LINENOS,
        dest="linenos",
        help="How to output linenos in source code. Three options availables: "
        "no (no line numbers); "
        "inline (inside <pre> tag); "
        "table (lines numbers in another cell, copy-paste friendly)",
        default="inline",
    )

    parser.add_option(
        "-o", "--direct-output",
        action="store_true",
        dest="direct",
        help="Prints the generated HTML code to stdout; won't work with PDF "
             "export",
        default=False)

    parser.add_option(
        "-P", "--no-presenter-notes",
        action="store_false",
        dest="presenter_notes",
        help="Don't include presenter notes in the output",
        default=True)

    parser.add_option(
        "-q", "--quiet",
        action="store_false",
        dest="verbose",
        help="Won't write anything to stdout (silent mode)",
        default=False)

    parser.add_option(
        "-r", "--relative",
        action="store_true",
        dest="relative",
        help="Make your presentation asset links relative to current pwd; "
             "This may be useful if you intend to publish your html "
             "presentation online.",
        default=False,
    )

    parser.add_option(
        "-t", "--theme",
        dest="theme",
        help="A theme name, or path to a landlside theme directory",
        default='default')

    parser.add_option(
        "-v", "--verbose",
        action="store_true",
        dest="verbose",
        help="Write informational messages to stdout (enabled by default)",
        default=True)

    parser.add_option(
        "-x", "--extensions",
        dest="extensions",
        help="Comma-separated list of extensions for Markdown",
        default='',
    )

    parser.add_option(
        "-w", "--watch",
        action="store_true",
        dest="watch",
        help="Watch source directory for changes and regenerate slides",
        default=False
    )

    parser.add_option(
        "-m", "--math-output",
        action="store_true",
        dest="math_output",
        help="Enable mathematical output using MathJax",
        default=False
    )

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    return options, args[0]


def log(message, type):
    """Log notices to stdout and errors to stderr"""

    (sys.stdout if type == 'notice' else sys.stderr).write(message + "\n")


def run(input_file, options):
    """Runs the Generator using parsed options."""

    options.logger = log
    generator.Generator(input_file, **options.__dict__).execute()


def main():
    """Main program entry point"""

    options, input_file = _parse_options()

    if (options.debug):
        run(input_file, options)
    else:
        try:
            run(input_file, options)
        except Exception as e:
            sys.stderr.write("Error: %s\n" % e)
            sys.exit(1)


if __name__ == '__main__':
    main()
