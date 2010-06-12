#!/usr/bin/env python

import os
import re
import glob
import codecs
import jinja2
import markdown
import pygments
import sys

from optparse import OptionParser
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

parser = OptionParser()
parser.add_option("-d", "--destination",
                  dest="destination_file",
                  help="The path to the to the destination",
                  metavar="FILE",
                  default="presentation.html")
parser.add_option("-e", "--encoding",
                  dest="encoding",
                  help="The encoding of your files (defaults to utf8)",
                  metavar="ENCODING",
                  default="utf8")
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
                  help="The path to the markdown source file, or a directory \
                        containing several files to combine",
                  metavar="FILE",
                  default="slides.md")
parser.add_option("-v", "--verbose",
                  action="store_true",
                  dest="verbose",
                  help="Write informational messages to stdin (enabled by  \
                        default)",
                  default=True)

(options, args) = parser.parse_args()

class Generator:
    def __init__(self, options, args):
        self.configure(options, args)
    
    def configure(self, options, args):
        """
        Configures this generator from its properties. "args" are not used (yet?)
        """
        self.direct = options.direct
        self.encoding = options.encoding
        self.verbose = options.verbose
        
        if (os.path.exists and not os.path.isfile(options.destination_file)):
            raise IOError("Destination %s exists and is not a file" % options.destination_file)
        else:
            self.destination_file = options.destination_file
        
        if (not os.access(self.destination_file, os.W_OK)):
            raise IOError("Destination file %s is not writeable" % self.destination_file)
        
        if (os.path.exists(options.source)):
            self.source = options.source
        else:
            raise IOError("Source file/directory %s does not exist" % options.source)

        if (os.path.exists(options.template_file)):
            self.template_file = options.template_file
        else:
            raise IOError("Template file %s does not exist" % options.template_file)

    def execute(self):
        """
        Execute this generator regarding its current configuration
        """
        if (self.direct):
            print self.render()
        else:
            self.write()
            self.log("Generated file: %s" % self.destination_file)

    def fetch_md_contents(self, source):
        """
        Recursively fetches Markdown contents from a single file or directories 
        containing Markdown files
        """
        self.log("Adding %s" % source)
        
        md_contents = ""
        
        if os.path.isdir(source):
            for md_file in glob.glob('%s/*.md' % source):
                md_contents = md_contents + self.fetch_md_contents(md_file)
        else:
            md_contents = codecs.open(source, encoding=self.encoding).read()

        return md_contents

    def get_template_vars(self, slides_src):
        """
        Computes template vars from slide source
        """
        head_title = slides_src[0].split('>')[1].split('<')[0]
        
        slides = []

        for slide_src in slides_src:
            header, content = slide_src.split('\n', 1)

            slides.append({'header': header, 
                           'content': self.highlight_code(content)})

        return {'head_title': head_title, 'slides': slides}

    def highlight_code(self, content):
        """
        Performs syntax coloration in code blocks
        """
        while '<code>!' in content:
            lang_match = re.search('<code>!(.+)\n', content)

            if lang_match:
                lang = lang_match.group(1)
                code = content.split(lang, 1)[1].split('</code', 1)[0]

                lexer = get_lexer_by_name(lang)

                formatter = HtmlFormatter(linenos='inline', noclasses=True,
                                          nobackground=True)

                pretty_code = pygments.highlight(code, lexer, formatter)
                pretty_code = pretty_code.replace('&amp;', '&')

                before_code = content.split('<code>', 1)[0]
                after_code = content.split('</code>', 1)[1]

                content = before_code + pretty_code + after_code

        return content

    def log(self, message):
        if (self.verbose):
            print message
    
    def render(self):
        """
        Returns generated html code
        """
        md_src = self.fetch_md_contents(self.source)

        slides_src = markdown.markdown(md_src).split('<hr />\n')

        template_src = codecs.open(self.template_file, encoding=self.encoding)
        template = jinja2.Template(template_src.read())
        
        return template.render(self.get_template_vars(slides_src))

    def write(self):
        """
        Writes generated presentation code into the destination file
        """
        outfile = codecs.open(self.destination_file, 'w', encoding=self.encoding)
        outfile.write(self.render())

try:
    Generator(options, args).execute()
except Exception as e:
    sys.exit("Error: %s" % e)
