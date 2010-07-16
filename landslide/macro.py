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

import re
import htmlentitydefs
import pygments

from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

RE_HTML_ENTITY = re.compile('&(\w+?);')


class Macro():
    def __init__(self, logger):
        self.logger = logger

    def process(self, content):
        """Generic processor (dioes actually nothing)"""
        return content, ''


class CodeHighlightingMacro(Macro):
    def descape(self, string, defs=htmlentitydefs.entitydefs):
        """Decodes html entities from a given string"""
        f = lambda m: defs[m.group(1)] if len(m.groups()) > 0 else m.group(0)
        return RE_HTML_ENTITY.sub(f, string)

    def process(self, content):
        """Performs syntax coloration in slide code blocks using Pygments"""
        code_blocks = re.findall(r'(<code>!(.+?)\n(.+?)</code>)', content,
                                 re.DOTALL | re.UNICODE)
        if not code_blocks:
            return content, ''

        classes = [u'has_code']
        for block, lang, code in code_blocks:
            try:
                lexer = get_lexer_by_name(lang)
            except Exception:
                self.logger(u"Unknown pygment lexer \"%s\", code "
                             "higlighting skipped for this block" % lang,
                            'warning')
                return content, ''
            formatter = HtmlFormatter(linenos='inline', noclasses=True,
                                      nobackground=True)
            pretty_code = pygments.highlight(self.descape(code), lexer,
                                             formatter)
            content = content.replace(block, pretty_code, 1)
        return content, classes


class FxMacro(Macro):
    def process(self, content):
        """Processes FXs"""
        classes = []
        fx_match = re.search(r'(<p>\.fx:\s?(.*?)</p>\n?)', content,
                             re.DOTALL | re.UNICODE)
        if fx_match:
            classes = fx_match.group(2).split(u' ')
            content = content.replace(fx_match.group(1), '', 1)
        return content, classes


class NotesMacro(Macro):
    def process(self, content):
        """Processes Notes"""
        classes = [u'has_notes']
        content = re.sub(r'<p>\.notes:\s?(.*?)</p>',
                         r'<p class="notes">\1</p>', content)
        return content, classes
