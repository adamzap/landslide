import os
import re
import codecs
import jinja2
import functools

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
            rendered_source = renderer.render(source)

            for html in re.split('<hr.+>', rendered_source):
                self.slides.append(Slide(html, source))

        self.get_css_files()
        self.get_js_files()

        self.write()

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

    def get_js_files(self):
        self.js_files = []

        theme_js_path = os.path.join(self.theme_dir, 'slides.js')

        if os.path.exists(theme_js_path):
            self.js_files.append(theme_js_path)

        if not self.js_files:
            default_js_path = os.path.join(THEMES_DIR, 'default', 'slides.js')

            self.js_files.append(default_js_path)

    def get_context(self):
        return {
            'slides': self.slides,
            'css_files': self.css_files,
            'js_files': self.js_files
        }

    def get_template_path(self):
        theme_path = os.path.join(self.theme_dir, 'base.html')
        default_path = os.path.join(THEMES_DIR, 'default', 'base.html')

        return theme_path if os.path.exists(theme_path) else default_path

    def write(self):
        open = functools.partial(codecs.open, encoding=self.options.encoding)

        template_path = self.get_template_path()

        with open(template_path) as template_file:
            template = jinja2.Template(template_file.read())

        html = template.render(self.get_context())

        with open(self.options.destination, 'w') as out_file:
            out_file.write(html)
