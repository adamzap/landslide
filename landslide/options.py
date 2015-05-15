from six.moves import configparser


class Options(object):
    def __init__(self, args):
        self.has_config_file = args['<source-or-config-file>'].endswith('.cfg')

        if self.has_config_file:
            self.parse_config_file(args['<source-or-config-file>'])

        self.parse_arguments(args)

    def parse_config_file(self, config_file):
        parser = configparser.RawConfigParser()
        parser.read(config_file)

        config = dict(parser.items('landslide'))
        config = {k: v for k, v in config.items() if v}

        self.sources = [s.strip() for s in config.get('source').split('\n')]

        self.theme = config.get('theme')
        self.destination = config.get('destination')
        self.linenos = config.get('linenos')
        self.extensions = config.get('extensions')
        self.css = config.get('css').split('\n')
        self.js = config.get('js').split('\n')

    def parse_arguments(self, args):
        if not self.has_config_file:
            self.sources.insert(0, args['<source-or-config-file>'])

        self.sources.extend(args['<source-files>'])

        for key in [k for k in args.keys() if k.startswith('--')]:
            obj_key = key.replace('--', '').replace('-', '_')

            if args[key]:
                setattr(self, obj_key, args[key])
