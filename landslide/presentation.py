import os

import renderer


class Presentation(object):
    def __init__(self, options):
        self.sources = self.flatten_sources(options.sources)
        self.options = options

        self.rendered_sources = []

        for source in self.sources:
            self.rendered_sources.append(renderer.render(source))

        self.write()

    def flatten_sources(self, sources):
        # TODO: Support deep dirs?
        flattened = []

        for source in sources:
            if os.path.isdir(source):
                flattened.extend(os.listdir(source))
            else:
                flattened.append(source)

        return flattened

    def write(self):
        pass
