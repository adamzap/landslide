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
import codecs
import jinja2
import tempfile
import sys
import utils
import ConfigParser

from macro import *
from parser import Parser
from subprocess import *


BASE_DIR = os.path.dirname(__file__)
THEMES_DIR = os.path.join(BASE_DIR, 'themes')
TOC_MAX_LEVEL = 2


class Generator(object):
    def __init__(self, source, destination_file='presentation.html',
                 theme='default', direct=False, debug=False, verbose=True,
                 embed=False, encoding='utf8', logger=None):
        """Configures this generator from its properties."""
        self.debug = debug
        self.direct = direct
        self.encoding = encoding
        self.logger = None
        self.num_slides = 0
        self.__toc = []

        # macros registering
        self.macros = []
        default_macros = [
            CodeHighlightingMacro,
            EmbedImagesMacro,
            FixImagePathsMacro,
            FxMacro,
            NotesMacro,
        ]
        for macro in default_macros:
            self.register_macro(macro)

        if logger:
            if callable(logger):
                self.logger = logger
            else:
                raise ValueError(u"Invalid logger set, must be a callable")
        self.verbose = False if direct else verbose and self.logger

        if source and os.path.exists(source):
            self.source_base_dir = os.path.split(os.path.abspath(source))[0]
            if source.endswith('.cfg'):
                self.log(u"Config   %s" % source)
                try:
                    config = ConfigParser.RawConfigParser()
                    config.read(source)
                except Exception, e:
                    raise RuntimeError(u"Invalid configuration file: %s" % e)
                self.source = (config.get('landslide', 'source')
                                     .replace('\r', '').split('\n'))
                if config.has_option('landslide', 'theme'):
                    theme = config.get('landslide', 'theme')
                    self.log(u"Using    configured theme %s" % theme)
                if config.has_option('landslide', 'destination'):
                    destination_file = config.get('landslide', 'destination')
            else:
                self.source = source
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
            raise IOError(u"This program can only write html or pdf files. "
                           "Please use one of these file extensions in the "
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
            default_dir = os.path.join(THEMES_DIR, 'default')

            if not os.path.exists(os.path.join(default_dir, 'base.html')):
                raise IOError(u"Cannot find base.html in default theme")
            else:
                self.template_file = os.path.join(default_dir, 'base.html')
        else:
            self.template_file = os.path.join(self.theme_dir, 'base.html')

    def add_toc_entry(self, title, level, slide_number):
        """Adds a new entry to current presentation Table of Contents"""
        self.__toc.append({'title': title, 'number': slide_number,
                           'level': level})

    def get_toc(self):
        """Smart getter for Table of Content list"""
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

    def execute(self):
        """Execute this generator regarding its current configuration"""
        if self.direct:
            if self.file_type is 'pdf':
                raise IOError(u"Direct output mode is not available for PDF "
                               "export")
            else:
                print self.render()
        else:
            self.write()
            self.log(u"Generated file: %s" % self.destination_file)

    def fetch_contents(self, source):
        """Recursively fetches Markdown contents from a single file or
        directory containing itself Markdown files
        """
        slides = []

        if type(source) is list:
            for entry in source:
                slides.extend(self.fetch_contents(entry))
        elif os.path.isdir(source):
            self.log(u"Entering %s" % source)
            for entry in os.listdir(source):
                slides.extend(self.fetch_contents(os.path.join(source, entry)))
        else:
            try:
                parser = Parser(os.path.splitext(source)[1], self.encoding)
            except NotImplementedError:
                return slides

            self.log(u"Adding   %s (%s)" % (source, parser.format))
            
            try:
                file_contents = codecs.open(source, encoding=self.encoding).read()
            except UnicodeDecodeError:
                self.log(u"Unable to decode source %s: skipping" % source, 'warning')
            else:
                inner_slides = re.split(r'<hr.+>', parser.parse(file_contents))
                for inner_slide in inner_slides:
                    slides.append(self.get_slide_vars(inner_slide, source))

        if not slides:
            self.log(u"Exiting  %s: no contents found" % source, 'notice')

        return slides

    def get_css(self):
        """Fetches and returns stylesheet file path or contents, for both print
        and screen contexts, depending if we want a standalone presentation or
        not
        """
        css = {}

        print_css = os.path.join(self.theme_dir, 'css', 'print.css')
        if not os.path.exists(print_css):
            # Fall back to default theme
            print_css = os.path.join(THEMES_DIR, 'default', 'css', 'print.css')

            if not os.path.exists(print_css):
                raise IOError(u"Cannot find css/print.css in default theme")

        css['print'] = {'path_url': utils.get_abs_path_url(print_css),
                        'contents': open(print_css).read()}


        screen_css = os.path.join(self.theme_dir, 'css', 'screen.css')
        if (os.path.exists(screen_css)):
            css['screen'] = {'path_url': utils.get_abs_path_url(screen_css),
                             'contents': open(screen_css).read()}
        else:
            self.log(u"No screen stylesheet provided in current theme",
                      'warning')

        return css

    def get_js(self):
        """Fetches and returns javascript file path or contents, depending if
        we want a standalone presentation or not
        """
        js_file = os.path.join(self.theme_dir, 'js', 'slides.js')

        if not os.path.exists(js_file):
            js_file = os.path.join(THEMES_DIR, 'default', 'js', 'slides.js')

            if not os.path.exists(js_file):
                raise IOError(u"Cannot find slides.js in default theme")

        return {'path_url': utils.get_abs_path_url(js_file),
                'contents': open(js_file).read()}

    def get_slide_vars(self, slide_src, source=None):
        """Computes a single slide template vars from its html source code.
           Also extracts slide informations for the table of contents.
        """
        vars = {'header': None, 'content': None}

        find = re.search(r'^\s?(<h(\d?)>(.+?)</h\d>)\s?(.+)?', slide_src,
                         re.DOTALL | re.UNICODE)
        if not find:
            header = level = title = None
            content = slide_src.strip()
        else:
            header = find.group(1)
            level = int(find.group(2))
            title = find.group(3)
            content = find.group(4).strip() if find.group(4) else find.group(4)

        slide_classes = []

        if content:
            content, slide_classes = self.process_macros(content, source)

        source_dict = {}

        if source:
            source_dict = {'rel_path': source,
                           'abs_path': os.path.abspath(source)}

        if header or content:
            return {'header': header, 'title': title, 'level': level,
                    'content': content, 'classes': slide_classes,
                    'source': source_dict}

    def get_template_vars(self, slides):
        """Computes template vars from slides html source code"""
        try:
            head_title = slides[0]['title']
        except (IndexError, TypeError):
            head_title = "Untitled Presentation"

        for slide_index, slide_vars in enumerate(slides):
            if not slide_vars:
                continue
            self.num_slides += 1
            slide_number = slide_vars['number'] = self.num_slides
            if slide_vars['level'] and slide_vars['level'] <= TOC_MAX_LEVEL:
                self.add_toc_entry(slide_vars['title'], slide_vars['level'],
                                   slide_number)

        return {'head_title': head_title, 'num_slides': str(self.num_slides),
                'slides': slides, 'toc': self.toc, 'embed': self.embed,
                'css': self.get_css(), 'js': self.get_js()}

    def log(self, message, type='notice'):
        """Log a message (eventually, override to do something more clever)"""
        if self.verbose and self.logger:
            self.logger(message, type)

    def process_macros(self, content, source=None):
        """Processed all macros"""
        classes = []
        for macro_class in self.macros:
            try:
                macro = macro_class(logger=self.logger, embed=self.embed)
                content, add_classes = macro.process(content, source)
                if add_classes:
                    classes += add_classes
            except Exception, e:
                self.log(u"%s processing failed in %s: %s"
                         % (macro, source, e))
        return content, classes

    def register_macro(self, macro_class):
        """Registers a new macro"""
        import inspect
        if (not inspect.isclass(macro_class)
            or not Macro in macro_class.__bases__):
            raise TypeError("A macro must inherit from landslide.macro.Macro")
        else:
            self.macros.append(macro_class)

    def render(self):
        """Returns generated html code"""
        template_src = codecs.open(self.template_file, encoding=self.encoding)
        template = jinja2.Template(template_src.read())
        slides = self.fetch_contents(self.source)
        return template.render(self.get_template_vars(slides))

    def write(self):
        """Writes generated presentation code into the destination file"""
        html = self.render()

        if self.file_type is 'pdf':
            self.write_pdf(html)
        else:
            outfile = codecs.open(self.destination_file, 'w',
                                  encoding='utf_8')
            outfile.write(html)

    def write_pdf(self, html):
        """Tries to write a PDF export from the command line using PrinceXML if
        available
        """
        try:
            f = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            f.write(html.encode('utf_8', 'xmlcharrefreplace'))
            f.close()
        except Exception:
            raise IOError(u"Unable to create temporary file, aborting")

        dummy_fh = open(os.path.devnull, 'w')

        try:
            command = ["prince", f.name, self.destination_file]

            process = Popen(command, stderr=dummy_fh).communicate()
        except Exception:
            raise EnvironmentError(u"Unable to generate PDF file using "
                                    "prince. Is it installed and available?")
        finally:
            dummy_fh.close()
