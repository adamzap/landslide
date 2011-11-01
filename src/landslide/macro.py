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
import htmlentitydefs
import pygments
import sys
import utils

from pygments.lexers import get_lexer_by_name
from pygments.lexers import get_lexer_for_filename
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter


class Macro(object):
    """Base class for Macros. A Macro aims to analyse, process and eventually
       alter some provided HTML contents and to provide supplementary
       informations to the slide context.
    """
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
    """This Macro performs syntax coloration in slide code blocks using
       Pygments.
    """
    code_blocks_re = re.compile(
        r'(<pre.+?>(<code>)?\s?!(\w+?)\n(.*?)(</code>)?</pre>)',
        re.UNICODE | re.MULTILINE | re.DOTALL)

    html_entity_re = re.compile('&(\w+?);')

    def descape(self, string, defs=None):
        """Decodes html entities from a given string"""
        if defs is None:
            defs = htmlentitydefs.entitydefs
        f = lambda m: defs[m.group(1)] if len(m.groups()) > 0 else m.group(0)
        return self.html_entity_re.sub(f, string)

    def process(self, content, source=None):
        code_blocks = self.code_blocks_re.findall(content)
        if not code_blocks:
            return content, []

        classes = []
        for block, void1, lang, code, void2 in code_blocks:
            try:
                lexer = get_lexer_by_name(lang)
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
    """This Macro extracts images url and embed them using the base64
       algorithm.
    """
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
                return content, classes

            content = content.replace(u"src=\"" + image_url,
                                      u"src=\"" + encoded_url, 1)

            self.logger(u"Embedded image %s" % image_url, 'notice')

        return content, classes


class FixImagePathsMacro(Macro):
    """This Macro replaces html image paths with fully qualified absolute
       urls.
    """
    relative = False

    def process(self, content, source=None):
        classes = []

        if self.embed:
            return content, classes
        base_path = utils.get_path_url(source, self.options.get('relative'))
        base_url = os.path.split(base_path)[0]

        images = re.findall(r'<img.*?src="(?!http://)(.*?)".*/?>', content,
            re.DOTALL | re.UNICODE)

        for image in images:
            full_path = os.path.join(base_url, image)

            content = content.replace(image, full_path)

        return content, classes


class FxMacro(Macro):
    """This Macro processes fx directives, ie adds specific css classes
       named after what the parser found in them.
    """
    def process(self, content, source=None):
        classes = []

        fx_match = re.search(r'(<p>\.fx:\s?(.*?)</p>\n?)', content,
                             re.DOTALL | re.UNICODE)
        if fx_match:
            classes = fx_match.group(2).split(u' ')
            content = content.replace(fx_match.group(1), '', 1)

        return content, classes


class NotesMacro(Macro):
    """This Macro processes Notes."""
    def process(self, content, source=None):
        classes = []

        new_content = re.sub(r'<p>\.notes:\s?(.*?)</p>',
                             r'<p class="notes">\1</p>', content)

        if content != new_content:
            classes.append(u'has_notes')

        return new_content, classes


class QRMacro(Macro):
    """This Macro generates a QR Code with Google Chart API."""
    def process(self, content, source=None):
        classes = []

        new_content = re.sub(r'<p>\.qr:\s?(\d*?)\|(.*?)</p>',
                             r'<p class="qr"><img src="http://chart.apis.google.com/chart?chs=\1x\1&cht=qr&chl=\2&chf=bg,s,00000000&choe=UTF-8" alt="QR Code" /></p>',
                             content)

        if content != new_content:
            classes.append(u'has_qr')

        return new_content, classes


class IncMacro(Macro):
    """This Macro includes the specified line or, range of lines of the given
       file as a highlighted code block or as is (raw HTML).
    """

    # Defaults
    INCLUDEPATH  = '.:./src:./code:..:../src:../code'
    EXPANDTABS   = 8

    # Macro pattern.
    include_re   = re.compile(
        r'(?P<leading><p>)(?P<macro>\.(code|coden|include):\s?)(?P<argline>.*?)(?P<trailing></p>\n?)',
        re.DOTALL | re.UNICODE)

    # Custom exception for proper error handling.
    class Error(Exception): pass

    def process(self, content, source=None):
        include_matches = self.include_re.finditer(content)
        if include_matches:
            self.options['expandtabs']  = self.options.get('expandtabs',
                                                        IncMacro.EXPANDTABS)
            self.options['includepath'] = self.options.get('includepath',
                                                        IncMacro.INCLUDEPATH)
            for match in include_matches:
                macro   = match.group('macro')
                argline = match.group('argline')
                context = macro + ' ' + argline

                try:
                    include_file, start, stop = self.parse_argline(argline)
                    found = self.locate_file(include_file, source)
                    if not found:
                        raise IncMacro.Error("couldn't locate file \"%s\" from include path \"%s\""
                                            % (include_file, self.options['includepath']))
                    include_file = found

                    include_content = self.get_lines(include_file, start, stop)

                    if '.code' in macro:
                        if '.coden' in macro:
                            # .coden
                            self.options['linenos'] = 'inline'
                            lineno_status = 'with linenos'
                        else:
                            # .code
                            self.options['linenos'] = False
                            lineno_status = ''
                        self.logger(u"Including file \"%s\" as code %s"
                                    % (include_file, lineno_status), 'notice')

                        try:
                            # Try to guess language from file extension.
                            lexer = get_lexer_for_filename(include_file)
                        except Exception:
                            try:
                                # Otherwise fallback to examine the file content.
                                # Note that this may produce wrong guesses for a small file.
                                lexer = guess_lexer(content)
                            except Exception:
                                self.logger(u"No available pygment lexer found; skipping highlighting",
                                            'warning')
                                return content

                        formatter = HtmlFormatter(linenos=self.options['linenos'],
                                                nobackground=True)
                        include_content = pygments.highlight(include_content, lexer, formatter)
                    else:
                        # .include
                        self.logger(u"Including file \"%s\" as is" % include_file, 'notice')

                    content = content.replace(match.group(0),
                                    match.group('leading') +
                                    include_content +
                                    match.group('trailing'), 1)
                except IncMacro.Error, e:
                    self.logger(u"Include error at \"%s\": %s" % (context, e), 'warning')
                except Exception, e:
                    self.logger(u"Unexpected error at \"%s\": %s; please report a bug"
                                % (context, e), 'warning')

        return content, []

    def parse_pattern(self, string):
        """Parse a pattern argument"""
        try:
            # Simple case: we have a line number.
            return int(string)
        except ValueError:
            pass

        # Otherwise we have a regular expression and (optionally) an offset

        prev = pattern = offset = ''
        start, stop = 0, len(string)
        if string[start] in '/':
            delim = string[start]
            start += 1
            for i, c in enumerate(string[start:]):
                if c == delim and prev != '\\':
                    stop = i+ start
                    break
                prev = c
            pattern, offset = string[start:stop], string[stop+1:]
        else:
            pattern = string

        compiled = None
        if pattern:
            try:
                compiled = re.compile(pattern, re.DOTALL | re.UNICODE)
            except Exception:
                raise IncMacro.Error("invalid pattern: \"%s\"" % string)

            if offset:
                m = re.search(r'(?P<sign>[+-]?)(?P<offset>\d*)', offset)
                if not m:
                    raise IncMacro.Error("invalid offset: \"%s\"" % string)
                sign, offset = m.group('sign'), m.group('offset')
                if offset:
                    try:
                        offset = int(offset)
                    except ValueError:
                        raise IncMacro.Error("invalid offset: \"%s\"" % string)
                else:
                    offset = 1 if sign else 0
                if sign == '-':
                    offset = -offset
            else:
                offset = 0

            return {
                'source': string,
                're'    : compiled,
                'offset': offset,
            }

    def parse_argline(self, argline):
        """Parse macro arguments"""
        # XXX Ugly hack to restore the special character '*' which rendered
        # to <em>...</em> when occured in pair.
        # For example: "/.*foo/ /.*bar/" becomes  "/.<em>foo/ /.</em>bar/
        if '<em>' in argline and '</em>' in argline:
            argline_fixed = re.sub(r'</?em>', '*', argline)
            self.logger(u"Argline \"%s\" was fixed as \"%s\""
                        % (argline, argline_fixed), 'warning')
            argline = argline_fixed

        path = start = stop = None
        args = iter(argline.split())
        try:
            path  = args.next()
            start = self.parse_pattern(args.next())
            stop  = self.parse_pattern(args.next())
        except StopIteration:
            pass

        if not path:
            raise IncMacro.Error("no include file specified")

        return path, start, stop

    def locate_file(self, path, source=None):
        """Locate the given file in includepath"""
        paths = self.options['includepath'].split(':')
        found = None
        if paths:
            curdir = os.path.dirname(source)
            if not curdir: curdir = "."
            for p in paths:
                f = os.path.normpath(os.path.join(curdir, p, path))
                if os.path.exists(f):
                    found = f
                    break
        else:
            raise IncMacro.Error("invalid include path: \"%s\""
                                 % self.option['includepath'])

        return found

    def index_matched(self, lines, start, pattern):
        """Identifies the line in lines that matches the pattern, starting from
           start.  Return value is 0-indexed.
        """
        max = len(lines)
        if pattern['source'] == '$':
            return max - 1

        found = None
        for i in range(start, max):
            if pattern['re'].match(lines[i]):
                found = i
                break
        if not found:
            raise IncMacro.Error("no matched line for pattern \"%s\""
                                 % pattern['source'])

        found += pattern['offset']
        if found < 0 or found >= max:
            raise IncMacro.Error("offset matched line is out of range [1-%d]" % max)

        return found


    def index_numbered(self, lines, num):
        """Converts a 1-indexed line number to a 0-indexed value."""
        max = len(lines)
        if abs(num) > max:
            raise IncMacro.Error("line %d is out of range [1-%d]" % (num, max))
        # note the semantics for negative line numbers
        return num - 1 if num > 0 else num

    def get_lines(self, path, start=None, stop=None):
        """Gets the lines of the file as a multiline string between the patterns
           start and stop.  Returns the whole file if no pattern given, one line
           if one argument given, and multiple lines if two patterns given.
        """
        f = open(path)
        lines = f.readlines()
        f.close()

        result = ""

        if start is None:
            # all lines
            result = "".join(lines)
        else:
            if stop is None:
                # one line
                if type(start) is int:
                    result = lines[self.index_numbered(lines, start)]
                else:
                    result = lines[self.index_matched(lines, 0, start)]
            else:
                # multi lines
                if type(start) is int:
                    start_index = self.index_numbered(lines, start)
                else:
                    start_index = self.index_matched(lines, 0, start)

                if type(stop) is int:
                    stop_index = self.index_numbered(lines, stop)
                else:
                    stop_index = self.index_matched(lines, start_index, stop)

                results = lines[
                    start_index:
                    # -1, which represents the file end, should not wrap up to 0
                    len(lines) if stop_index == -1 else stop_index + 1
                ]
                if results:
                    result = "".join(results)
                elif start_index >= stop_index:
                    raise IncMacro.Error("lines out of order in [%s, %s]" % (start, stop))

        tabsize = self.options['expandtabs']
        if tabsize > 0:
            result = result.expandtabs(tabsize)

        return result
