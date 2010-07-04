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

import os
import re
import glob
import base64
import codecs
import mimetypes
import jinja2
import pygments
import tempfile
import sys

from parser import Parser

from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from subprocess import *


BASE_DIR = os.path.dirname(__file__)
THEMES_DIR = os.path.join(BASE_DIR, 'themes')
TOC_MAX_LEVEL = 2


class Generator:
    def __init__(self, source, destination_file='presentation.html',
                 theme='default', direct=False, debug=False, verbose=True,
                 embed=False, encoding='utf8', logger=None):
        """Configures this generator from its properties. "args" are not used
        (yet?)
        """
        self.debug = debug
        self.direct = direct
        self.encoding = encoding
        self.logger = None
        self.num_slides = 0
        self.__toc = []

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

        self.embed = True if self.file_type is 'pdf' else embed

        self.theme = theme if theme else 'default'

        if os.path.exists(theme):
            self.theme_dir = theme
        elif os.path.exists(os.path.join(THEMES_DIR, theme)):
            self.theme_dir = os.path.join(THEMES_DIR, theme)
        else:
            raise IOError(u"Theme %s not found or invalid" % theme)

        if not os.path.exists(os.path.join(self.theme_dir, 'base.html')):
            raise IOError(u"Cannot find base.html template filein theme %s"
                          % theme)
        else:
            self.template_file = os.path.join(self.theme_dir, 'base.html')

    def add_toc_entry(self, title, level, slide_number):
        """Adds a new entry to current presentation Table of Contents
        """
        self.__toc.append({'title': title, 'number': slide_number,
                           'level': level})

    def get_toc(self):
        """Smart getter for Table of Content list
        """
        toc = []
        stack = [toc]
        for entry in self.__toc:
            entry['sub'] = []
            while entry['level'] < len(stack):
                stack.pop()
            while entry['level'] > len(stack):
                stack.append(stack[-1][-1]['sub'])
            stack[-1].append(entry)
        return toc

    def set_toc(self, value):
        raise ValueError("toc is read-only")

    toc = property(get_toc, set_toc)

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

            if image_url.startswith('file://'):
                self.log(u"%s: file:// image urls are not supported: skipped"
                         % from_source, 'warning')
                continue

            if (image_url.startswith('http://')
                or image_url.startswith('https://')):
                continue
            elif os.path.isabs(image_url):
                image_real_path = image_url
            else:
                image_real_path = os.path.join(os.path.dirname(from_source),
                                               image_url)

            if not os.path.exists(image_real_path):
                self.log(u"%s: image file %s not found: skipped"
                         % (from_source, image_real_path), 'warning')
                continue

            mime_type, encoding = mimetypes.guess_type(image_real_path)

            if not mime_type:
                self.log(u"%s: unknown image mime-type in %s: skipped"
                         % (from_source, image_real_path), 'warning')
                continue

            try:
                image_contents = open(image_real_path).read()
                encoded_image = base64.b64encode(image_contents)
            except IOError:
                self.log(u"%s: unable to read image %s: skipping"
                         % (from_source, image_real_path), 'warning')
                continue
            except Exception:
                self.log(u"%s: unable to base64-encode image %s: skipping"
                         % (from_source, image_real_path), 'warning')
                continue

            encoded_url = u"data:%s;base64,%s" % (mime_type, encoded_image)

            html_contents = html_contents.replace(image_url, encoded_url, 1)

            self.log(u"Embedded image %s" % image_real_path)

        return html_contents

    def execute(self):
        """Execute this generator regarding its current configuration
        """
        if self.direct:
            if self.file_type is 'pdf':
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
            self.log(u"Entering %s" % source)

            for entry in os.listdir(source):
                contents += self.fetch_contents(os.path.join(source, entry))
        else:
            try:
                parser = Parser(os.path.splitext(source)[1], self.encoding)
            except NotImplementedError:
                return contents
            
            self.log(u"Adding   %s (%s)" % (source, parser.format))

            file_contents = codecs.open(source, encoding=self.encoding).read()
            contents = parser.parse(file_contents)

            if self.embed:
                contents = self.embed_images(contents, source)

        if not contents.strip():
            self.log(u"No contents found in %s" % source, 'warning')

        return contents

    def get_css(self):
        """Fetches and returns stylesheet contents, for both print and screen
        contexts
        """
        css = {}

        print_css = os.path.join(self.theme_dir, 'css', 'print.css')
        if (os.path.exists(print_css)):
            css['print'] = open(print_css).read()

        screen_css = os.path.join(self.theme_dir, 'css', 'screen.css')
        if (os.path.exists(screen_css)):
            css['screen'] = open(screen_css).read()

        return css

    def get_js(self):
        """Fetches and returns javascript contents
        """
        js_file = os.path.join(self.theme_dir, 'js', 'slides.js')
        if (os.path.exists(js_file)):
            return open(js_file).read()

    def get_slide_vars(self, slide_src, slide_number):
        """Computes a single slide template vars from its html source code.
           Also extracts slide informations for the table of contents.
        """
        vars = {'header': None, 'content': None}

        find = re.search(r'^\s?(<h(\d?)>(.+?)</h\d>)\s?(.+)?', slide_src,
                         re.DOTALL | re.UNICODE)
        if not find:
            header = None
            content = slide_src
        else:
            header = find.group(1)
            level = int(find.group(2))
            title = find.group(3)
            content = find.group(4)
            if level <= TOC_MAX_LEVEL:
                self.add_toc_entry(title, level, slide_number)

        if content:
            content = self.highlight_code(content.strip())

        self.num_slides += 1

        return {'header': header, 'content': content, 'number': slide_number}

    def get_template_vars(self, slides_src):
        """Computes template vars from slides html source code
        """
        try:
            head_title = slides_src[0].split('>')[1].split('<')[0]
        except IndexError:
            head_title = "Untitled Presentation"

        slides = []

        for slide_index, slide_src in enumerate(slides_src):
            slide_number = slide_index + 1
            slide_vars = self.get_slide_vars(slide_src.strip(), slide_number)
            if not slide_vars['header'] and not slide_vars['content']:
                self.log(u"empty slide contents, skipping")
                continue
            slides.append(slide_vars)

        return {'head_title': head_title, 'slides': slides,
                'num_slides': str(self.num_slides), 'toc': self.toc,
                'css': self.get_css(), 'js': self.get_js()}

    def highlight_code(self, content):
        """Performs syntax coloration in slide code blocks
        """
        while u'<code>!' in content:
            code_match = re.search(r'<code>!(.+?)\n(.+?)</code>', content,
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
        slides_src = re.split(r'<hr.*?/>', self.fetch_contents(self.source))

        template_src = codecs.open(self.template_file, encoding=self.encoding)
        template = jinja2.Template(template_src.read())
        template_vars = self.get_template_vars(slides_src)

        return template.render(template_vars)

    def write(self):
        """Writes generated presentation code into the destination file
        """
        html = self.render()

        if self.file_type is 'pdf':
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
