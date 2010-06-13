# -*- coding: utf-8 -*-

import os
import re
import glob
import codecs
import jinja2
import markdown
import pygments
import tempfile

from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from subprocess import *


class Generator:
    def __init__(self, options, args):
        self.configure(options, args)

    def configure(self, options, args):
        """
        Configures this generator from its properties. "args" are not used
        (yet?)
        """
        self.direct = options.direct
        self.encoding = options.encoding
        self.verbose = False if options.direct else options.verbose

        if (os.path.exists(options.destination_file)
            and not os.path.isfile(options.destination_file)):
            raise IOError(u"Destination %s exists and is not a file"
                          % options.destination_file)
        else:
            self.destination_file = options.destination_file

        if (self.destination_file.endswith('.html')):
            self.file_type = 'html'
        elif (self.destination_file.endswith('.pdf')):
            self.file_type = 'pdf'
        else:
            raise IOError(u"This program can only write html or pdf files, "
                           "please use one of these file extensions in the "
                           "destination")

        if (os.path.exists(options.source)):
            self.source = options.source
        else:
            raise IOError(u"Source file/directory %s does not exist"
                          % options.source)

        if (os.path.exists(options.template_file)):
            self.template_file = options.template_file
        else:
            raise IOError(u"Template file %s does not exist"
                          % options.template_file)

    def execute(self):
        """
        Execute this generator regarding its current configuration
        """
        if (self.direct):
            if (self.file_type == 'pdf'):
                raise IOError(u"Direct output mode is not available for PDF "
                               "export")
            else:
                print self.render()
        else:
            self.write()
            self.log(u"Generated file: %s" % self.destination_file)

    def fetch_md_contents(self, source):
        """
        Recursively fetches Markdown contents from a single file or directory
        containing itself Markdown files
        """
        self.log(u"Adding %s" % source)

        md_contents = ""

        if os.path.isdir(source):
            for entry in os.listdir(source):
                current = os.path.join(source, entry)
                if os.path.isdir(current):
                    md_contents = md_contents + self.fetch_md_contents(current)
                elif current.endswith('.md') or current.endswith('.markdown'):
                    md_contents = md_contents + self.fetch_md_contents(current)
        else:
            md_contents = codecs.open(source, encoding=self.encoding).read()

        if not md_contents.strip():
            raise ValueError("No Markdown contents found")

        return md_contents

    def get_template_vars(self, slides_src):
        """
        Computes template vars from slide source
        """
        try:
            head_title = slides_src[0].split('>')[1].split('<')[0]
        except IndexError:
            head_title = "Untitled Presentation"

        slides = []

        for slide_src in slides_src:
            if not slide_src.strip():
                continue
            
            try:
                header, content = slide_src.split('\n', 1)
            except ValueError:
                header = None
                content = slide_src

            slides.append({'header': header, 
                           'content': self.highlight_code(content)})

        return {'head_title': head_title, 'slides': slides}

    def highlight_code(self, content):
        """
        Performs syntax coloration in slide code blocks
        """

        while u'<code>!' in content:
            code_match = re.search('<code>!(.+?)\n(.+?)</code>', content,
                                   re.DOTALL)

            if code_match:
                lang, code = code_match.groups()

                code = code.replace('&lt;', '<').replace('&gt;', '>')

                lexer = get_lexer_by_name(lang)

                formatter = HtmlFormatter(linenos='inline', noclasses=True,
                                          nobackground=True)

                pretty_code = pygments.highlight(code, lexer, formatter)
                pretty_code = pretty_code.replace('&amp;', '&')

                before_code = content.split(u'<code>', 1)[0]
                after_code = content.split(u'</code>', 1)[1]

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

        slides_src = markdown.markdown(md_src).split(u'<hr />\n')

        template_src = codecs.open(self.template_file, encoding=self.encoding)
        template = jinja2.Template(template_src.read())

        return template.render(self.get_template_vars(slides_src))

    def write(self):
        """
        Writes generated presentation code into the destination file
        """
        html = self.render()

        if (self.file_type == 'pdf'):
            self.write_pdf(html)
        else:
            outfile = codecs.open(self.destination_file, 'w',
                                  encoding=self.encoding)
            outfile.write(html)

    def write_pdf(self, html):
        """
        Tries to write a PDF export from the command line using PrinceXML if
        available
        """
        try:
            f = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            f.write(html.encode(self.encoding))
            f.close()
        except Exception:
            raise IOError(u"Unable to create temporary file")

        try:
            command = Popen(["prince", f.name, self.destination_file])
        except Exception:
            raise EnvironmentError(u"Unable to generate PDF file using prince."
                                    "Is it installed and available?")
