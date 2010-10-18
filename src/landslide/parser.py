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
    'markdown':         ['.mdown', '.markdown', '.markdn', '.md'],
    'restructuredtext': ['.rst', '.rest'],
}


class Parser(object):
    def __init__(self, extension, encoding='utf-8'):
        """Configures this parser"""
        self.encoding = encoding
        self.format = None
        for supp_format, supp_extensions in SUPPORTED_FORMATS.items():
            for supp_extension in supp_extensions:
                if supp_extension == extension:
                    self.format = supp_format
        if not self.format:
            raise NotImplementedError(u"Unsupported format %s" % extension)

    def parse(self, text):
        """Parses and renders a text as HTML regarding current format"""
        if self.format == 'markdown':
            try:
                import markdown
            except ImportError:
                raise RuntimeError(u"Looks like markdown is not installed")

            return markdown.markdown(text)
        elif self.format == 'restructuredtext':
            try:
                from rst import html_parts, html_body
            except ImportError:
                raise RuntimeError(u"Looks like docutils are not installed")

            html = html_body(text, input_encoding=self.encoding,
                                   output_encoding=self.encoding)
            html = re.sub(r'<div.*?>\n', r'', html, re.DOTALL | re.UNICODE)
            html = re.sub(r'</div>\n', r'', html, re.DOTALL | re.UNICODE)
            html = re.sub(r'<p class="sys.+\n.+ion\.', r'', html,
                          re.DOTALL | re.UNICODE) # Pretty hackish
            html = re.sub(r'<h1 class="title">', r'<h1>', html,
                          re.DOTALL | re.UNICODE)
            html = re.sub(r'<hr class=".*?" />\n', r'<hr />\n', html,
                          re.DOTALL | re.UNICODE)

            return html
        else:
            raise NotImplementedError(u"Unsupported format %s, cannot parse"
                                      % self.format)
