# -*- coding: utf-8 -*-

import os
import re
import sys
import pygments
import html.entities

from . import utils

from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class Macro(object):
    """Base class for altering slide HTML during presentation generation"""

    options = {}

    def __init__(self, logger=sys.stdout, embed=False, options=None):
        self.logger = logger
        self.embed = embed
        if options:
            if not isinstance(options, dict):
                raise ValueError(u'Macro options must be a dict instance')
            self.options = options

    def process(self, content, source=None):
        """Generic processor (does actually nothing)"""
        return content, []


class CodeHighlightingMacro(Macro):
    """Performs syntax coloration in slide code blocks using Pygments"""

    code_blocks_re = re.compile(
        r'(<pre.+?>(<code>)?\s?!(\S+?)\n(.*?)(</code>)?</pre>)',
        re.UNICODE | re.MULTILINE | re.DOTALL)

    html_entity_re = re.compile('&(\w+?);')

    def descape(self, string, defs=None):
        """Decodes html entities from a given string"""
        if defs is None:
            defs = html.entities.entitydefs
        f = lambda m: defs[m.group(1)] if len(m.groups()) > 0 else m.group(0)
        return self.html_entity_re.sub(f, string)

    def process(self, content, source=None):
        code_blocks = self.code_blocks_re.findall(content)
        if not code_blocks:
            return content, []

        classes = []
        for block, void1, lang, code, void2 in code_blocks:
            try:
                lexer = get_lexer_by_name(lang, startinline=True)
            except Exception:
                self.logger(u"Unknown pygment lexer \"%s\", skipping"
                            % lang, 'warning')
                return content, classes

            if 'linenos' not in self.options or self.options['linenos'] =='no':
                self.options['linenos'] = False

            formatter = HtmlFormatter(linenos=self.options['linenos'],
                                      nobackground=True)
            pretty_code = pygments.highlight(self.descape(code), lexer,
                                             formatter)
            content = content.replace(block, pretty_code, 1)

        return content, [u'has_code']


class EmbedImagesMacro(Macro):
    """Encodes images in base64 for embedding in image:data"""

    def process(self, content, source=None):
        classes = []

        if not self.embed:
            return content, classes

        images = re.findall(r'<img\s.*?src="(.+?)"\s?.*?/?>', content,
                            re.DOTALL | re.UNICODE)

        source_dir = os.path.dirname(source)

        for image_url in images:
            encoded_url = utils.encode_image_from_url(image_url, source_dir)

            if not encoded_url:
                self.logger(u"Failed to embed image \"%s\"" % image_url, 'warning')
                return content, classes

            content = content.replace(u"src=\"" + image_url,
                                      u"src=\"" + encoded_url, 1)

            self.logger(u"Embedded image %s" % image_url, 'notice')

        return content, classes


class FixImagePathsMacro(Macro):
    """Replaces html image paths with fully qualified absolute urls"""

    relative = False

    def process(self, content, source=None):
        classes = []

        if self.embed:
            return content, classes

        base_path = utils.get_path_url(source, self.options.get('relative'))
        base_url = os.path.split(base_path)[0]

        regex = r'<img.*?src="(?!https?://|file://)(.*?)".*?/?>'

        images = re.findall(regex, content, re.DOTALL | re.UNICODE)

        for image in list(set(images)):
            full_path = '"' + os.path.join(base_url, image) + '"'
            image = '"' + image + '"'

            content = content.replace(image, full_path)

        return content, classes


class FxMacro(Macro):
    """Adds custom CSS class to slides"""

    def process(self, content, source=None):
        classes = []

        fx_match = re.search(r'(<p>\.fx:\s?(.*?)</p>\n?)', content,
                             re.DOTALL | re.UNICODE)
        if fx_match:
            classes = fx_match.group(2).split(u' ')
            content = content.replace(fx_match.group(1), '', 1)

        return content, classes


class NotesMacro(Macro):
    """Adds toggleable notes to slides"""

    def process(self, content, source=None):
        classes = []

        new_content = re.sub(r'<p>\.notes:\s?(.*?)</p>',
                             r'<p class="notes">\1</p>', content)

        if content != new_content:
            classes.append(u'has_notes')

        return new_content, classes


class QRMacro(Macro):
    """Generates a QR code in a slide"""

    def process(self, content, source=None):
        classes = []

        new_content = re.sub(r'<p>\.qr:\s?(\d*?)\|(.*?)</p>',
                             r'<p class="qr"><img src="https://chart.apis.google.com/chart?chs=\1x\1&cht=qr&chl=\2&chf=bg,s,00000000&choe=UTF-8" alt="QR Code" /></p>',
                             content)

        if content != new_content:
            classes.append(u'has_qr')

        return new_content, classes
