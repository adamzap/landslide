# -*- coding: utf-8 -*-

import os
import re
import glob
import base64
import codecs
import mimetypes
import jinja2
import markdown
import pygments
import tempfile
import sys

from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from subprocess import *


BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


class Generator:
    def __init__(self, source, destination_file='presentation.html',
                 template_file=None, direct=False, debug=False, verbose=True,
                 embed=False, encoding='utf8', logger=None):
        """Configures this generator from its properties. "args" are not used
        (yet?)
        """
        self.debug = debug
        self.direct = direct
        self.encoding = encoding
        self.logger = None

        if logger:
            if callable(logger):
                self.logger = logger
            else:
                raise ValueError(u"Invalid logger set, must be a callable")
        self.verbose = False if direct else verbose and self.logger

        if source and os.path.exists(source):
            self.source = source
            self.source_base_dir = os.path.split(os.path.abspath(source))[0]
        else:
            raise IOError(u"Source file/directory %s does not exist"
                          % source)

        if (os.path.exists(destination_file)
            and not os.path.isfile(destination_file)):
            raise IOError(u"Destination %s exists and is not a file"
                          % destination_file)
        else:
            self.destination_file = destination_file

        if self.destination_file.endswith('.html'):
            self.file_type = 'html'
        elif self.destination_file.endswith('.pdf'):
            self.file_type = 'pdf'
        else:
            raise IOError(u"This program can only write html or pdf files, "
                           "please use one of these file extensions in the "
                           "destination")

        self.embed = True if self.file_type == 'pdf' else embed

        if not template_file:
            template_file = os.path.join(TEMPLATE_DIR, 'base.html')

        if os.path.exists(template_file):
            self.template_file = template_file
        else:
            raise IOError(u"Template file %s does not exist" % template_file)

    def embed_images(self, html_contents, from_source):
        """Extracts images url and embed them using the base64 algorithm
        """
        images = re.findall(r'<img\s.*?src="(.+?)"\s?.*?/?>', html_contents,
                            re.DOTALL | re.UNICODE)

        if not images:
            return html_contents

        for image_url in images:
            if not image_url or image_url.startswith('data:'):
                continue

            if image_url.startswith('file:///'):
                self.log(u"Warning: file:/// image urls are not supported: "
                          "skipped", 'warning')
                continue

            if (image_url.startswith('http://')
                or image_url.startswith('https://')):
                continue
            elif os.path.isabs(image_url):
                image_real_path = image_url
            else:
                image_real_path = os.path.join(os.path.dirname(from_source), image_url)

            if not os.path.exists(image_real_path):
                self.log(u"Warning: image file %s not found: skipped"
                         % image_real_path, 'warning')
                continue

            mime_type, encoding = mimetypes.guess_type(image_real_path)

            if not mime_type:
                self.log(u"Warning: unknown image mime-type (%s): skipped"
                         % image_real_path, 'warning')
                continue

            try:
                image_contents = open(image_real_path).read()
                encoded_image = base64.b64encode(image_contents)
            except IOError:
                self.log(u"Warning: unable to read image contents %s: skipping"
                         % image_real_path, 'warning')
                continue
            except Exception:
                self.log(u"Warning: unable to base64-encode image %s: skipping"
                         % image_real_path, 'warning')
                continue

            encoded_url = u"data:%s;base64,%s" % (mime_type, encoded_image)

            html_contents = html_contents.replace(image_url, encoded_url, 1)

            self.log(u"Embedded image %s" % image_real_path)

        return html_contents

    def execute(self):
        """Execute this generator regarding its current configuration
        """
        if self.direct:
            if self.file_type == 'pdf':
                raise IOError(u"Direct output mode is not available for PDF "
                               "export")
            else:
                print self.render().encode(self.encoding)
        else:
            self.write()
            self.log(u"Generated file: %s" % self.destination_file)

    def fetch_contents(self, source):
        """Recursively fetches Markdown contents from a single file or
        directory containing itself Markdown files
        """
        contents = ""

        if os.path.isdir(source):
            self.log(u"Entering %s/" % source)

            for entry in os.listdir(source):
                current = os.path.join(source, entry)
                if (os.path.isdir(current) or current.endswith('.md')
                    or current.endswith('.markdown')):
                    contents = contents + self.fetch_contents(current)
        else:
            self.log(u"Adding   %s" % source)

            md_contents = codecs.open(source, encoding=self.encoding).read()
            contents = markdown.markdown(md_contents)
            if self.embed:
                contents = self.embed_images(contents, source)

        if not contents.strip():
            self.log(u"No contents found in %s" % source, 'warning')

        return contents

    def get_slide_vars(self, slide_src):
        """Computes a single slide template vars from its html source code
        """
        vars = {'header': None, 'content': None}
        
        find = re.search(r'^\s?(<h\d?>.+?</h\d>)\s?(.+)?', slide_src, 
                         re.DOTALL | re.UNICODE)
        
        if not find:
            header = None
            content = slide_src
        else:
            header = find.group(1)
            content = find.group(2)
            
        if content:
            content = self.highlight_code(content.strip())
        
        return {'header': header, 'content': content}

    def get_template_vars(self, slides_src):
        """Computes template vars from slides html source code
        """
        try:
            head_title = slides_src[0].split('>')[1].split('<')[0]
        except IndexError:
            head_title = "Untitled Presentation"

        slides = []

        for slide_src in slides_src:
            slide_vars = self.get_slide_vars(slide_src.strip())
            if not slide_vars['header'] and not slide_vars['content']:
                self.log(u"empty slide contents, skipping")
                continue
            slides.append(slide_vars)

        return {'head_title': head_title, 'slides': slides}

    def highlight_code(self, content):
        """Performs syntax coloration in slide code blocks
        """
        while u'<code>!' in content:
            code_match = re.search('<code>!(.+?)\n(.+?)</code>', content,
                                   re.DOTALL)

            if code_match:
                lang, code = code_match.groups()

                code = code.replace('&lt;', '<').replace('&gt;', '>')
                code = code.replace('&amp;', '&')

                try:
                    lexer = get_lexer_by_name(lang)
                except Exception:
                    self.log(u"Unknown pygment lexer \"%s\", code higlighting "
                              "skipped" % lang)
                    continue

                formatter = HtmlFormatter(linenos='inline', noclasses=True,
                                          nobackground=True)

                pretty_code = pygments.highlight(code, lexer, formatter)

                before_code = content.split(u'<code>', 1)[0]
                after_code = content.split(u'</code>', 1)[1]

                content = before_code + pretty_code + after_code

        return content

    def log(self, message, type='notice'):
        """Log a message (eventually, override to do something more clever)
        """
        if self.verbose and self.logger:
            self.logger(message, type)

    def render(self):
        """Returns generated html code
        """
        slides_src = self.fetch_contents(self.source).split(u'<hr />')

        template_src = codecs.open(self.template_file, encoding=self.encoding)
        template = jinja2.Template(template_src.read())
        template_vars = self.get_template_vars(slides_src)

        return template.render(template_vars)

    def write(self):
        """Writes generated presentation code into the destination file
        """
        html = self.render()

        if self.file_type == 'pdf':
            self.write_pdf(html)
        else:
            outfile = codecs.open(self.destination_file, 'w',
                                  encoding=self.encoding)
            outfile.write(html)

    def write_pdf(self, html):
        """Tries to write a PDF export from the command line using PrinceXML if
        available
        """
        try:
            f = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            f.write(html.encode(self.encoding))
            f.close()
        except Exception:
            raise IOError(u"Unable to create temporary file, aborting")

        dummy_fh = open(os.path.devnull, 'w')

        try:
            command = ["prince", f.name, self.destination_file]

            process = Popen(command, stderr=dummy_fh).communicate()
        except Exception:
            raise EnvironmentError(u"Unable to generate PDF file using prince."
                                    "Is it installed and available?")
        finally:
            dummy_fh.close()
