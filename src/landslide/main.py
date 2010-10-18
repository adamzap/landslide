#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2010 Adam Zapletal
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys

try:
    from landslide.generator import Generator
except ImportError:
    from generator import Generator

from optparse import OptionParser

def _parse_options():
    """parses ``landslide`` args options"""

    parser = OptionParser(
        usage="%prog [options] input.md ...",
        description="Generates an HTML5 or PDF "
                    "slideshow from Markdown or other formats",
        epilog="Note: PDF export requires the `prince` program: "
               "http://princexml.com/"
        )

    parser.add_option(
        "-b", "--debug",
        action="store_true",
        dest="debug",
        help="Will display any exception trace to stdin",
        default=False
    )

    parser.add_option(
        "-d", "--destination",
        dest="destination_file",
        help="The path to the to the destination file: .html or "
             ".pdf extensions allowed (default: presentation.html)",
        metavar="FILE",
        default="presentation.html"
    )

    parser.add_option(
        "-e", "--encoding",
        dest="encoding",
        help="The encoding of your files (defaults to utf-8)",
        metavar="ENCODING",
        default="utf-8"
    )

    parser.add_option(
        "-i", "--embed",
        action="store_true",
        dest="embed",
        help="Embed stylesheet and javascript contents, "
             "base64-encoded images in presentation to make a "
             "standalone document",
        default=False
    )

    parser.add_option(
        "-t", "--theme",
        dest="theme",
        help="A theme name, or path to a landlside theme directory",
        default='default'
    )

    parser.add_option(
        "-o", "--direct-ouput",
        action="store_true",
        dest="direct",
        help="Prints the generated HTML code to stdin; won't work "
             "with PDF export",
        default=False
    )

    parser.add_option(
        "-q", "--quiet",
        action="store_false",
        dest="verbose",
        help="Won't write anything to stdin (silent mode)",
        default=False
    )

    parser.add_option(
        "-v", "--verbose",
        action="store_true",
        dest="verbose",
        help="Write informational messages to stdin (enabled by "
        "default)",
        default=True
    )

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    return options, args[0]


def log(message, type):
    (sys.stdout if type == 'notice' else sys.stderr).write(message + "\n")


def run(input_file, options):
    generator = Generator(input_file, options.destination_file,
                          options.theme, direct=options.direct,
                          debug=options.debug, verbose=options.verbose,
                          embed=options.embed, encoding=options.encoding,
                          logger=log)
    generator.execute()


def main():
    options, input_file = _parse_options()
    
    if (options.debug):
        run(input_file, options)
    else:
        try:
            run(input_file, options)
        except Exception, e:
            sys.stderr.write("Error: %s\n" % e)
            sys.exit(1)


if __name__ == '__main__':
    main()
