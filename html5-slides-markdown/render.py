#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from generator import Generator
from optparse import OptionParser

parser = OptionParser(usage="%prog [options] input.md ...",
                      description="Generates fancy HTML5 or PDF slideshows "
                                  "from Markdown sources ",
                      epilog="Note: PDF export requires the `prince` program: "
                             "http://princexml.com/")
parser.add_option("-b", "--debug",
                  action="store_true",
                  dest="debug",
                  help="Will display any exception trace to stdin",
                  default=False)
parser.add_option("-d", "--destination",
                  dest="destination_file",
                  help="The path to the to the destination file: .html or "
                       ".pdf extensions allowed (default: presentation.html)",
                  metavar="FILE",
                  default="presentation.html")
parser.add_option("-e", "--encoding",
                  dest="encoding",
                  help="The encoding of your files (defaults to utf8)",
                  metavar="ENCODING",
                  default="utf8")
parser.add_option("-i", "--embed",
                  action="store_true",
                  dest="embed",
                  help="Embed base64-encoded images in presentation",
                  default=False)
parser.add_option("-t", "--template",
                  dest="template_file",
                  help="The path to a Jinja2 compatible template file",
                  metavar="FILE",
                  default=None)
parser.add_option("-o", "--direct-ouput",
                  action="store_true",
                  dest="direct",
                  help="Prints the generated HTML code to stdin; won't work "
                       "with PDF export",
                  default=False)
parser.add_option("-q", "--quiet",
                  action="store_false",
                  dest="verbose",
                  help="Won't write anything to stdin (silent mode)",
                  default=False)
parser.add_option("-v", "--verbose",
                  action="store_true",
                  dest="verbose",
                  help="Write informational messages to stdin (enabled by "
                       "default)",
                  default=True)

(options, args) = parser.parse_args()

if not args:
    parser.print_help()
    sys.exit(1)


def log(message, type):
    if type == 'notice':
        return sys.stdout.write(message + "\n")
    else:
        return sys.stderr.write(message + "\n")


def run():
    generator = Generator(args[0], options.destination_file,
                          options.template_file, direct=options.direct,
                          debug=options.debug, verbose=options.verbose,
                          embed=options.embed, encoding=options.encoding,
                          logger=log)
    generator.execute()

if __name__ == '__main__':
    if (options.debug):
        run()
    else:
        try:
            run()
        except Exception, e:
            sys.stderr.write("Error: %s\n" % e)
            sys.exit(1)
