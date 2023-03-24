# -*- coding: utf-8 -*-

import os
import re
import codecs
import inspect
import jinja2
import shutil
import tempfile
import configparser

from subprocess import Popen

from . import utils
from . import macro as macro_module
from .parser import Parser


BASE_DIR = os.path.dirname(__file__)
THEMES_DIR = os.path.join(BASE_DIR, 'themes')
TOC_MAX_LEVEL = 2
VALID_LINENOS = ('no', 'inline', 'table')


class Generator(object):
    """The Generator class takes and processes presentation source as a file, a
       folder or a configuration file and provides methods to render them as a
       presentation.
    """
    DEFAULT_DESTINATION = 'presentation.html'
    default_macros = [
        macro_module.CodeHighlightingMacro,
        macro_module.EmbedImagesMacro,
        macro_module.FixImagePathsMacro,
        macro_module.FxMacro,
        macro_module.NotesMacro,
        macro_module.QRMacro,
    ]
    user_css = []
    user_js = []

    def __init__(self, source, **kwargs):
        """ Configures this generator. Available ``args`` are:
            - ``source``: source file or directory path
            Available ``kwargs`` are:
            - ``copy_theme``: copy theme directory and files into presentation
                              one
            - ``destination_file``: path to html or PDF destination file
            - ``direct``: enables direct rendering presentation to stdout
            - ``debug``: enables debug mode
            - ``embed``: generates a standalone document, with embedded assets
            - ``encoding``: the encoding to use for this presentation
            - ``extensions``: Comma separated list of markdown extensions
            - ``logger``: a logger lambda to use for logging
            - ``presenter_notes``: enable presenter notes
            - ``relative``: enable relative asset urls
            - ``theme``: path to the theme to use for this presentation
            - ``verbose``: enables verbose output
        """
        self.copy_theme = kwargs.get('copy_theme', False)
        self.debug = kwargs.get('debug', False)
        self.destination_file = kwargs.get('destination_file',
                                           'presentation.html')
        self.direct = kwargs.get('direct', False)
        self.embed = kwargs.get('embed', False)
        self.encoding = kwargs.get('encoding', 'utf8')
        self.extensions = kwargs.get('extensions', None)
        self.logger = kwargs.get('logger', None)
        self.presenter_notes = kwargs.get('presenter_notes', True)
        self.relative = kwargs.get('relative', False)
        self.theme = kwargs.get('theme', 'default')
        self.verbose = kwargs.get('verbose', False)
        self.linenos = self.linenos_check(kwargs.get('linenos'))
        self.watch = kwargs.get('watch', False)
        self.math_output = kwargs.get('math_output', False)
        self.num_slides = 0
        self.__toc = []

        # macros registering
        self.macros = []
        self.register_macro(*self.default_macros)

        if self.direct:
            # Only output html in direct output mode, not log messages
            self.verbose = False

        if not source or not os.path.exists(source):
            raise IOError(u"Source file/directory %s does not exist"
                          % source)

        if source.endswith('.cfg'):
            config = self.parse_config(source)
            self.source = config.get('source')
            if not self.source:
                raise IOError('unable to fetch a valid source from config')
            source_abspath = os.path.abspath(self.source[0])
            self.destination_file = config.get('destination',
                self.DEFAULT_DESTINATION)
            self.embed = config.get('embed', False)
            self.relative = config.get('relative', False)
            self.copy_theme = config.get('copy_theme', False)
            self.extensions = config.get('extensions', '')
            self.theme = config.get('theme', 'default')
            self.add_user_css(config.get('css', []))
            self.add_user_js(config.get('js', []))
            self.linenos = self.linenos_check(config.get('linenos'))
        else:
            self.source = source
            source_abspath = os.path.abspath(source)

        if not os.path.isdir(source_abspath):
            source_abspath = os.path.dirname(source_abspath)

        self.watch_dir = source_abspath

        if (os.path.exists(self.destination_file)
            and not os.path.isfile(self.destination_file)):
            raise IOError(u"Destination %s exists and is not a file"
                          % self.destination_file)

        if self.destination_file.endswith('.html'):
            self.file_type = 'html'
        elif self.destination_file.endswith('.pdf'):
            self.file_type = 'pdf'
            self.embed = True
        else:
            raise IOError(u"This program can only write html or pdf files. "
                           "Please use one of these file extensions in the "
                           "destination")

        self.theme_dir = self.find_theme_dir(self.theme, self.copy_theme)
        self.template_file = self.get_template_file()

    def add_user_css(self, css_list):
        """ Adds supplementary user css files to the presentation. The
            ``css_list`` arg can be either a ``list`` or a string.
        """
        if isinstance(css_list, str):
            css_list = [css_list]

        for css_path in css_list:
            if css_path and css_path not in self.user_css:
                if not os.path.exists(css_path):
                    raise IOError('%s user css file not found' % (css_path,))
                with codecs.open(css_path, encoding=self.encoding) as css_file:
                    self.user_css.append({
                        'path_url': utils.get_path_url(css_path,
                                                       self.relative),
                        'contents': css_file.read(),
                    })

    def add_user_js(self, js_list):
        """ Adds supplementary user javascript files to the presentation. The
            ``js_list`` arg can be either a ``list`` or a string.
        """
        if isinstance(js_list, str):
            js_list = [js_list]
        for js_path in js_list:
            if js_path and js_path not in self.user_js:
                if js_path.startswith("http:"):
                    self.user_js.append({
                        'path_url': js_path,
                        'contents': '',
                    })
                elif not os.path.exists(js_path):
                    raise IOError('%s user js file not found' % (js_path,))
                else:
                    with codecs.open(js_path,
                                     encoding=self.encoding) as js_file:
                        self.user_js.append({
                            'path_url': utils.get_path_url(js_path,
                                                           self.relative),
                            'contents': js_file.read(),
                        })

    def add_toc_entry(self, title, level, slide_number):
        """ Adds a new entry to current presentation Table of Contents.
        """
        self.__toc.append({'title': title, 'number': slide_number,
                           'level': level})

    @property
    def toc(self):
        """ Smart getter for Table of Content list.
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

    def execute(self):
        """ Execute this generator regarding its current configuration.
        """
        if self.direct:
            if self.file_type == 'pdf':
                raise IOError(u"Direct output mode is not available for PDF "
                               "export")
            else:
                print(self.render().encode(self.encoding))
        else:
            self.write_and_log()

            if self.watch:
                from landslide.watcher import watch

                self.log(u"Watching %s\n" % self.watch_dir)

                watch(self.watch_dir, self.write_and_log)

    def write_and_log(self):
        self.watch_files = []
        self.num_slides = 0
        self.__toc = []
        self.write()
        self.log(u"Generated file: %s" % self.destination_file)

    def get_template_file(self):
        """ Retrieves Jinja2 template file path.
        """
        if os.path.exists(os.path.join(self.theme_dir, 'base.html')):
            return os.path.join(self.theme_dir, 'base.html')
        default_dir = os.path.join(THEMES_DIR, 'default')
        if not os.path.exists(os.path.join(default_dir, 'base.html')):
            raise IOError(u"Cannot find base.html in default theme")
        return os.path.join(default_dir, 'base.html')

    def fetch_contents(self, source):
        """ Recursively fetches Markdown contents from a single file or
            directory containing itself Markdown files.
        """
        slides = []

        if type(source) is list:
            for entry in source:
                slides.extend(self.fetch_contents(entry))
        elif os.path.isdir(source):
            self.log(u"Entering %s" % source)
            entries = os.listdir(source)
            entries.sort()
            for entry in entries:
                slides.extend(self.fetch_contents(os.path.join(source, entry)))
        else:
            try:
                parser = Parser(os.path.splitext(source)[1], self.encoding,
                    self.extensions)
            except NotImplementedError:
                return slides

            self.log(u"Adding   %s (%s)" % (source, parser.format))

            try:
                with codecs.open(source, encoding=self.encoding) as file:
                    file_contents = file.read()
            except UnicodeDecodeError:
                self.log(u"Unable to decode source %s: skipping" % source,
                         'warning')
            else:
                inner_slides = re.split(r'<hr.+>', parser.parse(file_contents))
                for inner_slide in inner_slides:
                    slides.append(self.get_slide_vars(inner_slide, source))

        if not slides:
            self.log(u"Exiting  %s: no contents found" % source, 'notice')

        return slides

    def find_theme_dir(self, theme, copy_theme=False):
        """ Finds them dir path from its name.
        """
        if os.path.exists(theme):
            self.theme_dir = theme
        elif os.path.exists(os.path.join(THEMES_DIR, theme)):
            self.theme_dir = os.path.join(THEMES_DIR, theme)
        else:
            raise IOError(u"Theme %s not found or invalid" % theme)
        target_theme_dir = os.path.join(os.getcwd(), 'theme')
        if copy_theme or os.path.exists(target_theme_dir):
            self.log(u'Copying %s theme directory to %s'
                     % (theme, target_theme_dir))
            if not os.path.exists(target_theme_dir):
                try:
                    shutil.copytree(self.theme_dir, target_theme_dir)
                except Exception as e:
                    self.log(u"Skipped copy of theme folder: %s" % e)
                    pass
            self.theme_dir = target_theme_dir
        return self.theme_dir

    def get_css(self):
        """ Fetches and returns stylesheet file path or contents, for both
            print and screen contexts, depending if we want a standalone
            presentation or not.
        """
        css = {}

        print_css = os.path.join(self.theme_dir, 'css', 'print.css')

        if not os.path.exists(print_css):
            # Fall back to default theme
            print_css = os.path.join(THEMES_DIR, 'default', 'css', 'print.css')

            if not os.path.exists(print_css):
                raise IOError(u"Cannot find css/print.css in default theme")

        with codecs.open(print_css, encoding=self.encoding) as css_file:
            css['print'] = {
                'path_url': utils.get_path_url(print_css, self.relative),
                'contents': css_file.read(),
            }

        screen_css = os.path.join(self.theme_dir, 'css', 'screen.css')

        if (os.path.exists(screen_css)):
            with codecs.open(screen_css, encoding=self.encoding) as css_file:
                css['screen'] = {
                    'path_url': utils.get_path_url(screen_css, self.relative),
                    'contents': css_file.read(),
                }
        else:
            self.log(u"No screen stylesheet provided in current theme",
                      'warning')

        return css

    def get_js(self):
        """ Fetches and returns javascript file path or contents, depending if
            we want a standalone presentation or not.
        """
        js_file = os.path.join(self.theme_dir, 'js', 'slides.js')

        if not os.path.exists(js_file):
            js_file = os.path.join(THEMES_DIR, 'default', 'js', 'slides.js')

            if not os.path.exists(js_file):
                raise IOError(u"Cannot find slides.js in default theme")
        with codecs.open(js_file, encoding=self.encoding) as js_file_obj:
            return {
                'path_url': utils.get_path_url(js_file, self.relative),
                'contents': js_file_obj.read(),
            }

    def get_slide_vars(self, slide_src, source=None):
        """ Computes a single slide template vars from its html source code.
            Also extracts slide informations for the table of contents.
        """
        presenter_notes = None

        find = re.search(r'<h\d[^>]*>presenter notes</h\d>', slide_src,
                         re.DOTALL | re.UNICODE | re.IGNORECASE)

        if find:
            if self.presenter_notes:
                presenter_notes = slide_src[find.end():].strip()

            slide_src = slide_src[:find.start()]

        find = re.search(r'(<h(\d+?).*?>(.+?)</h\d>)\s?(.+)?', slide_src,
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

        if header:
            header, _ = self.process_macros(header, source)

        if content:
            content, slide_classes = self.process_macros(content, source)

        source_dict = {}

        if source:
            source_dict = {'rel_path': source,
                           'abs_path': os.path.abspath(source)}

        if header or content:
            return {'header': header, 'title': title, 'level': level,
                    'content': content, 'classes': slide_classes,
                    'source': source_dict, 'presenter_notes': presenter_notes,
                    'math_output': self.math_output}

    def get_template_vars(self, slides):
        """ Computes template vars from slides html source code.
        """
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
            else:
                # Put something in the TOC even if it doesn't have a title or level
                self.add_toc_entry(u"-", 1, slide_number)

        return {'head_title': head_title, 'num_slides': str(self.num_slides),
                'slides': slides, 'toc': self.toc, 'embed': self.embed,
                'css': self.get_css(), 'js': self.get_js(),
                'user_css': self.user_css, 'user_js': self.user_js,
                'math_output': self.math_output}

    def linenos_check(self, value):
        """ Checks and returns a valid value for the ``linenos`` option.
        """
        return value if value in VALID_LINENOS else 'inline'

    def log(self, message, type='notice'):
        """ Logs a message (eventually, override to do something more clever).
        """
        if self.logger and not callable(self.logger):
            raise ValueError(u"Invalid logger set, must be a callable")
        if self.verbose and self.logger:
            self.logger(message, type)

    def parse_config(self, config_source):
        """ Parses a landslide configuration file and returns a normalized
            python dict.
        """
        self.log(u"Config   %s" % config_source)
        try:
            raw_config = configparser.RawConfigParser()
            raw_config.read(config_source)
        except Exception as e:
            raise RuntimeError(u"Invalid configuration file: %s" % e)
        config = {}
        config['source'] = raw_config.get('landslide', 'source')\
            .replace('\r', '').split('\n')
        if raw_config.has_option('landslide', 'theme'):
            config['theme'] = raw_config.get('landslide', 'theme')
            self.log(u"Using    configured theme %s" % config['theme'])
        if raw_config.has_option('landslide', 'destination'):
            config['destination'] = raw_config.get('landslide', 'destination')
        if raw_config.has_option('landslide', 'linenos'):
            config['linenos'] = raw_config.get('landslide', 'linenos')
        for boolopt in ('embed', 'relative', 'copy_theme'):
            if raw_config.has_option('landslide', boolopt):
                config[boolopt] = raw_config.getboolean('landslide', boolopt)
        if raw_config.has_option('landslide', 'extensions'):
            config['extensions'] = ",".join(raw_config.get('landslide', 'extensions')\
                .replace('\r', '').split('\n'))
        if raw_config.has_option('landslide', 'css'):
            config['css'] = raw_config.get('landslide', 'css')\
                .replace('\r', '').split('\n')
        if raw_config.has_option('landslide', 'js'):
            config['js'] = raw_config.get('landslide', 'js')\
                .replace('\r', '').split('\n')
        return config

    def process_macros(self, content, source=None):
        """ Processed all macros.
        """
        macro_options = {'relative': self.relative, 'linenos': self.linenos}
        classes = []
        for macro_class in self.macros:
            try:
                macro = macro_class(logger=self.logger, embed=self.embed,
                    options=macro_options)
                content, add_classes = macro.process(content, source)
                if add_classes:
                    classes += add_classes
            except Exception as e:
                self.log(u"%s processing failed in %s: %s"
                         % (macro, source, e))
        return content, classes

    def register_macro(self, *macros):
        """ Registers macro classes passed a method arguments.
        """
        for m in macros:
            if inspect.isclass(m) and issubclass(m, macro_module.Macro):
                self.macros.append(m)
            else:
                raise TypeError("Coundn't register macro; a macro must inherit"
                                " from macro.Macro")

    def render(self):
        """ Returns generated html code.
        """
        with codecs.open(self.template_file, encoding=self.encoding) as template_src:
            template = jinja2.Template(template_src.read())
        slides = self.fetch_contents(self.source)
        context = self.get_template_vars(slides)

        html = template.render(context)

        if self.embed:
            images = re.findall(r'url\(["\']?(.*?\.(?:jpe?g|gif|png|svg)[\'"]?)\)',
                html, re.DOTALL | re.UNICODE)

            for img_url in images:
                img_url = img_url.replace('"', '').replace("'", '')
                if self.theme_dir:
                    source = os.path.join(self.theme_dir, 'css')
                else:
                    source = os.path.join(THEMES_DIR, self.theme, 'css')

                encoded_url = utils.encode_image_from_url(img_url, source)
                if encoded_url:
                    html = html.replace(img_url, encoded_url, 1)
                    self.log("Embedded theme image %s from theme directory %s" % (img_url, source))
                else:
                    # Missing file in theme directory. Try user_css folders
                    found = False
                    for css_entry in context['user_css']:
                        directory = os.path.dirname(css_entry['path_url'])
                        if not directory:
                            directory = "."

                        encoded_url = utils.encode_image_from_url(img_url, directory)

                        if encoded_url:
                            found = True
                            html = html.replace(img_url, encoded_url, 1)
                            self.log("Embedded theme image %s from directory %s" % (img_url, directory))

                    if not found:
                        # Missing image file, etc...
                        self.log(u"Failed to embed theme image %s" % img_url)

        return html

    def write(self):
        """ Writes generated presentation code into the destination file.
        """
        html = self.render()

        if self.file_type == 'pdf':
            self.write_pdf(html)
        else:
            with codecs.open(self.destination_file, 'w',
                             encoding='utf_8') as outfile:
                outfile.write(html)

    def write_pdf(self, html):
        """ Tries to write a PDF export from the command line using Prince if
            available.
        """
        try:
            f = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            f.write(html.encode('utf_8', 'xmlcharrefreplace'))
            f.close()
        except Exception:
            raise IOError(u"Unable to create temporary file, aborting")

        dummy_fh = open(os.path.devnull, 'w')

        try:
            command = ["prince", f.name, "-o", self.destination_file]

            Popen(command, stderr=dummy_fh).communicate()
        except Exception:
            raise EnvironmentError(u"Unable to generate PDF file using "
                                    "prince. Is it installed and available?")
        finally:
            dummy_fh.close()
