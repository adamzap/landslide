import os

import renderer


class Presentation(object):
    def __init__(self, options):
        self.options = options

        self.sources = []
        self.rendered_sources = []

        for source in options.sources:
            self.add_source(source)

        for source in self.sources:
            self.rendered_sources.append(renderer.render(source))

        self.write()

    def add_source(self, source, prefix=''):
        path = os.path.join(prefix, source)

        if os.path.isdir(path):
            for f in os.listdir(path):
                self.add_source(f, path)
        else:
            self.sources.append(path)

    def write(self):
        pass
