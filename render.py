#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from generator import Generator
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-b", "--debug",
                  action="store_true",
                  dest="debug",
                  help="Will display any exception trace to stdin",
                  default=False)
parser.add_option("-d", "--destination",
                  dest="destination_file",
                  help="The path to the to the destination file: .html or "
                       ".pdf extensions allowed",
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
                  help="The path to the to the Jinja2 template file",
                  metavar="FILE",
                  default="base.html")
parser.add_option("-o", "--direct-ouput",
                  action="store_true",
                  dest="direct",
                  help="Prints the generated HTML code to stdin",
                  default=False)
parser.add_option("-q", "--quiet",
                  action="store_false",
                  dest="verbose",
                  help="Won't write anything to stdin",
                  default=False)
parser.add_option("-s", "--source",
                  dest="source",
                  help="The path to the markdown source file, or a directory "
                       "containing several files to combine",
                  metavar="FILE",
                  default="slides.md")
parser.add_option("-v", "--verbose",
                  action="store_true",
                  dest="verbose",
                  help="Write informational messages to stdin (enabled by "
                       "default)",
                  default=True)

(options, args) = parser.parse_args()

if (options.debug):
    Generator(options, args).execute()
else:
    try:
        Generator(options, args).execute()
    except Exception, e:
        sys.exit("Error: %s" % e)
