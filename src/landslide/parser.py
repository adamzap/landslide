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

SUPPORTED_FORMATS = {
    'markdown':         ['.mdown', '.markdown', '.markdn', '.md', '.mdn', '.mdwn'],
    'restructuredtext': ['.rst', '.rest'],
    'textile':          ['.textile'],
}


class Parser(object):
    """This class generates the HTML code depending on which syntax is used in
       the souce document.

       The Parser currently supports both Markdown and restructuredText
       syntaxes.
    """
    RST_REPLACEMENTS = [
            (r'<div.*?>', r'', re.UNICODE),
            (r'</div>', r'', re.UNICODE),
            (r'<p class="system-message-\w+">.*?</p>', r'', re.UNICODE),
            (r'Document or section may not begin with a transition\.',
             r'', re.UNICODE),
            (r'<h(\d+?).*?>', r'<h\1>', re.DOTALL | re.UNICODE),
            (r'<hr.*?>\n', r'<hr />\n', re.DOTALL | re.UNICODE),
    ]
    md_extensions = ''

    def __init__(self, extension, encoding='utf8', md_extensions=''):
        """Configures this parser.
        """
        self.encoding = encoding
        self.format = None
        for supp_format, supp_extensions in SUPPORTED_FORMATS.items():
            for supp_extension in supp_extensions:
                if supp_extension == extension:
                    self.format = supp_format
        if not self.format:
            raise NotImplementedError(u"Unsupported format %s" % extension)
        if md_extensions:
            exts = (value.strip() for value in md_extensions.split(','))
            self.md_extensions = filter(None, exts)

    def parse(self, text):
        """Parses and renders a text as HTML regarding current format.
        """
        if self.format == 'markdown':
            try:
                import markdown
            except ImportError:
                raise RuntimeError(u"Looks like markdown is not installed")

            if text.startswith(u'\ufeff'):  # check for unicode BOM
              text = text[1:]

            return markdown.markdown(text, self.md_extensions)
        elif self.format == 'restructuredtext':
            try:
                from rst import html_body
            except ImportError:
                raise RuntimeError(u"Looks like docutils are not installed")
            html = html_body(text, input_encoding=self.encoding)
            # RST generates pretty much markup to be removed in our case
            for (pattern, replacement, mode) in self.RST_REPLACEMENTS:
                html = re.sub(re.compile(pattern, mode), replacement, html, 0)
            return html.strip()
        elif self.format == 'textile':
            try:
                import textile
            except ImportError:
                raise RuntimeError(u"Looks like textile is not installed")

            return textile.textile(text, encoding=self.encoding)
        else:
            raise NotImplementedError(u"Unsupported format %s, cannot parse"
                                      % self.format)
