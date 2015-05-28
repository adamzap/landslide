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

    def get_context(self):
        # TODO: Refactor and flatten css and js variables in theme HTML
        return {
            'slides': self.slides,
            'css': {
                'print': {
                    'path_url': os.path.join(self.theme_dir, 'css', 'print.css')
                },
                'screen': {
                    'path_url': os.path.join(self.theme_dir, 'css', 'screen.css')
                }
            },
            'js': {
                'path_url': os.path.join(self.theme_dir, 'js', 'slides.js')
            }
        }

    def write(self):
        open = functools.partial(codecs.open, encoding=self.options.encoding)

        with open(os.path.join(self.theme_dir, 'base.html')) as template_file:
            template = jinja2.Template(template_file.read())

        html = template.render(self.get_context())

        with open(self.options.destination, 'w') as out_file:
            out_file.write(html)
