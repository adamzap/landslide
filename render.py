#!/usr/bin/env python
import codecs
import glob
import jinja2
import markdown
import pygments
import os
import re

from optparse import OptionParser
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

parser = OptionParser()
parser.add_option("-s", "--source", 
                  dest="source", 
                  help="The path to the markdown source file", 
                  metavar="FILE", 
                  default="slides.md")
parser.add_option("-d", "--destination", 
                  dest="destination_file", 
                  help="The path to the to the destination", 
                  metavar="FILE", 
                  default="presentation.html")
parser.add_option("-t", "--template", 
                  dest="template_file", 
                  help="The path to the to the Jinja2 template file", 
                  metavar="FILE", 
                  default="base.html")
parser.add_option("-e", "--encoding", 
                  dest="encoding", 
                  help="The encoding of your files (defaults to utf8)", 
                  metavar="ENCODING", 
                  default="utf8")
parser.add_option("-o", "--direct-ouput", 
                  action="store_true",
                  dest="direct", 
                  help="Prints the generated HTML code to stdin", 
                  default=False)

(options, args) = parser.parse_args()

class Generator:
    def __init__(self, options, args):
        self.direct = options.direct
        self.destination_file = options.destination_file
        self.encoding = options.encoding
        self.source = options.source
        self.template_file = options.template_file
    
    def execute(self):
        """
        Execute this generator configured process
        """
        if (self.direct):
            print self.render()
        else:
            self.write()
            print "Generated file: %s" % self.destination_file
    
    def fetch_md_contents(self, source):
        """
        Fetches Mardown contents from a single file, or a directory containing Mardown 
        files
        """
        print "Adding %s" % source
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
        template_vars = {}
        
        title = template_vars['title'] = slides_src.pop(0)

        template_vars['head_title'] = title.split('>')[1].split('<')[0]

        template_vars['slides'] = []

        for slide_src in slides_src:
            header, content = slide_src.split('\n', 1)

            content = self.highlight_code(content)

            template_vars['slides'].append({'header': header, 'content': content})
        
        return template_vars
    
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

Generator(options, args).execute()