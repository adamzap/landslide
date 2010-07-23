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
import base64
import htmlentitydefs
import mimetypes
import pygments
import sys
import utils

from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


RE_HTML_ENTITY = re.compile('&(\w+?);')


class Macro(object):
    def __init__(self, logger=sys.stdout, embed=False):
        self.logger = logger
        self.embed = embed

    def process(self, content, source=None):
        """Generic processor (does actually nothing)"""
        return content, []


class CodeHighlightingMacro(Macro):
    def descape(self, string, defs=htmlentitydefs.entitydefs):
        """Decodes html entities from a given string"""
        f = lambda m: defs[m.group(1)] if len(m.groups()) > 0 else m.group(0)
        return RE_HTML_ENTITY.sub(f, string)

    def process(self, content, source=None):
        """Performs syntax coloration in slide code blocks using Pygments"""
        code_blocks = re.findall(r'(<pre><code>!(.+?)\n(.+?)</code></pre>)',
                                 content, re.DOTALL | re.UNICODE)
        if not code_blocks:
            return content, []

        classes = []
        for block, lang, code in code_blocks:
            try:
                lexer = get_lexer_by_name(lang)
            except Exception:
                self.logger(u"Unknown pygment lexer \"%s\", skipping"
                            % lang, 'warning')
                return content, classes
            formatter = HtmlFormatter(linenos='inline', noclasses=True,
                                      nobackground=True)
            pretty_code = pygments.highlight(self.descape(code), lexer,
                                             formatter)
            content = content.replace(block, pretty_code, 1)

        return content, [u'has_code']


class EmbedImagesMacro(Macro):
    def process(self, content, source=None):
        """Extracts images url and embed them using the base64 algorithm"""
        classes = []

        if not self.embed:
            return content, classes

        images = re.findall(r'<img\s.*?src="(.+?)"\s?.*?/?>', content,
                            re.DOTALL | re.UNICODE)

        if not images:
            return content, []

        for image_url in images:
            if not image_url or image_url.startswith('data:'):
                continue

            if image_url.startswith('file://'):
                self.logger(u"%s: file:// image urls are not supported: "
                             "skipped" % source, 'warning')
                continue

            if (image_url.startswith('http://')
                or image_url.startswith('https://')):
                continue
            elif os.path.isabs(image_url):
                image_real_path = image_url
            else:
                image_real_path = os.path.join(os.path.dirname(source),
                                               image_url)

            if not os.path.exists(image_real_path):
                self.logger(u"%s: image file %s not found: skipped"
                            % (source, image_real_path), 'warning')
                continue

            mime_type, encoding = mimetypes.guess_type(image_real_path)

            if not mime_type:
                self.logger(u"%s: unknown image mime-type in %s: skipped"
                            % (source, image_real_path), 'warning')
                continue

            try:
                image_contents = open(image_real_path).read()
                encoded_image = base64.b64encode(image_contents)
            except IOError:
                self.logger(u"%s: unable to read image %s: skipping"
                            % (source, image_real_path), 'warning')
                continue
            except Exception:
                self.logger(u"%s: unable to base64-encode image %s: skipping"
                            % (source, image_real_path), 'warning')
                continue

            encoded_url = u"data:%s;base64,%s" % (mime_type, encoded_image)

            content = content.replace(image_url, encoded_url, 1)

            self.logger(u"Embedded image %s" % image_real_path, 'notice')

        return content, classes


class FixImagePathsMacro(Macro):
    def process(self, content, source=None):
        """Replaces html image paths with fully qualified absolute urls"""
        classes = []

        if self.embed:
            return content, classes

        base_url = os.path.split(utils.get_abs_path_url(source))[0]
        fn = lambda p: r'<img src="%s" />' % os.path.join(base_url, p.group(1))
        content = re.sub(r'<img.*?src="(.*?)".*/?>', fn, content, re.UNICODE)

        return content, classes


class FxMacro(Macro):
    def process(self, content, source=None):
        """Processes FXs"""
        classes = []

        fx_match = re.search(r'(<p>\.fx:\s?(.*?)</p>\n?)', content,
                             re.DOTALL | re.UNICODE)
        if fx_match:
            classes = fx_match.group(2).split(u' ')
            content = content.replace(fx_match.group(1), '', 1)

        return content, classes


class NotesMacro(Macro):
    def process(self, content, source=None):
        """Processes Notes"""
        classes = []

        new_content = re.sub(r'<p>\.notes:\s?(.*?)</p>',
                             r'<p class="notes">\1</p>', content)

        if content != new_content:
            classes.append(u'has_notes')

        return new_content, classes
