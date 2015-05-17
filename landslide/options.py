from six.moves import configparser


class Options(object):
    theme = 'default'
    linenos = 'inline'
    encoding = 'utf8'
    destination = 'presentation.html'

    js = css = extensions = []

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return False

    def __init__(self, args):
        self.has_config_file = args['<source-or-config-file>'].endswith('.cfg')

        if self.has_config_file:
            self.parse_config_file(args['<source-or-config-file>'])

        self.parse_arguments(args)

        if self.js:
            self.js = self.js.split('\n')

        if self.css:
            self.css = self.css.split('\n')

        if self.extensions:
            self.extensions = self.extensions.split(',')

    def parse_config_file(self, config_file):
        parser = configparser.RawConfigParser()
        parser.read(config_file)

        config = dict(parser.items('landslide'))
        config = {k: v for k, v in config.items() if v}

        self.sources = [s.strip() for s in config.get('source').split('\n')]

        self.theme = config.get('theme', self.theme)
        self.linenos = config.get('linenos', self.linenos)
        self.destination = config.get('destination', self.destination)
        self.encoding = config.get('encoding', self.encoding)
        self.extensions = config.get('extensions', self.extensions)
        self.css = config.get('css', self.css)
        self.js = config.get('js', self.js)
        self.copy_theme = config.get('copy_theme')
        self.debug = config.get('debug')
        self.embed = config.get('embed')
        self.direct_output = config.get('direct_output')
        self.no_presenter_notes = config.get('no_presenter_notes')
        self.quiet = config.get('quiet')
        self.relative = config.get('relative')
        self.watch = config.get('watch')
        self.math_output = config.get('math_output')

    def parse_arguments(self, args):
        if not self.has_config_file:
            self.sources = [args['<source-or-config-file>']]

        self.sources.extend(args['<source-files>'])

        for key in [k for k in args.keys() if k.startswith('--')]:
            obj_key = key.replace('--', '').replace('-', '_')

            if args[key]:
                setattr(self, obj_key, args[key])
