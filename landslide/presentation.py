import os
import re
import codecs
import jinja2

import renderer

from slide import Slide


THEMES_DIR = os.path.join(os.path.dirname(__file__), 'themes')


class Presentation(object):
    def __init__(self, options):
        self.options = options

        self.set_theme_dir()

        self.sources = []
        self.slides = []

        for source in options.sources:
            self.add_source(source)

        for source in self.sources:
            content = self.open(source).read()
            rendered_source = renderer.render(source, content)

            for html in re.split('<hr.+>', rendered_source):
                self.slides.append(Slide(html, source))

        self.get_css_files()
        self.get_js_files()

        self.write()

    def open(self, path, mode='r'):
        return codecs.open(path, mode, encoding=self.options.encoding)

    def set_theme_dir(self):
        theme = self.options.theme

        if os.path.exists(theme):
            self.theme_dir = theme
        elif os.path.exists(os.path.join(THEMES_DIR, theme)):
            self.theme_dir = os.path.join(THEMES_DIR, theme)
        else:
            raise Exception('Theme not found: %s', theme)

    def add_source(self, source, prefix=''):
        path = os.path.join(prefix, source)

        if os.path.isdir(path):
            for f in os.listdir(path):
                self.add_source(f, path)
        else:
            self.sources.append(path)

    def get_css_files(self):
        self.css_files = []

        theme_css_path = os.path.join(self.theme_dir, 'style.css')

        if os.path.exists(theme_css_path):
            self.css_files.append(theme_css_path)

        if not self.css_files:
            default_css_path = os.path.join(THEMES_DIR, 'default', 'style.css')

            self.css_files.append(default_css_path)

        self.css_files.extend(self.options.css)

    def get_js_files(self):
        self.js_files = [
            os.path.join(THEMES_DIR, 'default', 'jquery.js')
        ]

        theme_js_path = os.path.join(self.theme_dir, 'slides.js')

        if os.path.exists(theme_js_path):
            self.js_files.append(theme_js_path)

        if len(self.js_files) == 1:
            default_js_path = os.path.join(THEMES_DIR, 'default', 'slides.js')

            self.js_files.append(default_js_path)

        self.js_files.extend(self.options.js)

    def get_context(self):
        if self.options.embed:
            self.css_files = [self.open(f).read() for f in self.css_files]
            self.js_files = [self.open(f).read() for f in self.js_files]

        return {
            'slides': self.slides,
            'options': self.options,
            'css_files': self.css_files,
            'js_files': self.js_files
        }

    def get_template_path(self):
        theme_path = os.path.join(self.theme_dir, 'slides.html')
        default_path = os.path.join(THEMES_DIR, 'default', 'slides.html')

        return theme_path if os.path.exists(theme_path) else default_path

    def write(self):
        template_path = self.get_template_path()

        with self.open(template_path) as template_file:
            template = jinja2.Template(template_file.read())

        html = template.render(self.get_context())

        with self.open(self.options.destination, 'w') as out_file:
            out_file.write(html)
