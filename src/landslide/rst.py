# -*- coding: utf-8 -*-
#
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

from docutils import core, nodes
from docutils.parsers.rst import directives, Directive

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer


DEFAULT = HtmlFormatter(noclasses=False)
VARIANTS = {}


class Pygments(Directive):
    """ Source code syntax hightlighting for ReST syntax."""
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = dict([(key, directives.flag) for key in VARIANTS])
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()
        # take an arbitrary option if more than one is given
        formatter = (self.options and VARIANTS[self.options.keys()[0]]
                     or DEFAULT)
        parsed = highlight(u'\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]


directives.register_directive('sourcecode', Pygments)
directives.register_directive('code-block', Pygments)


def html_parts(input_string, source_path=None, destination_path=None,
               input_encoding='unicode', doctitle=1, initial_header_level=1):
    """
    Given an input string, returns a dictionary of HTML document parts.

    Dictionary keys are the names of parts, and values are Unicode strings;
    encoding is up to the client.

    Parameters:

    - `input_string`: A multi-line text string; required.
    - `source_path`: Path to the source file or object.  Optional, but useful
      for diagnostic output (system messages).
    - `destination_path`: Path to the file or object which will receive the
      output; optional.  Used for determining relative paths (stylesheets,
      source links, etc.).
    - `input_encoding`: The encoding of `input_string`.  If it is an encoded
      8-bit string, provide the correct encoding.  If it is a Unicode string,
      use "unicode", the default.
    - `doctitle`: Disable the promotion of a lone top-level section title to
      document title (and subsequent section title to document subtitle
      promotion); enabled by default.
    - `initial_header_level`: The initial level for header elements (e.g. 1
      for "<h1>").
    """
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level}
    parts = core.publish_parts(
        source=input_string, source_path=source_path,
        destination_path=destination_path,
        writer_name='html', settings_overrides=overrides)
    return parts


def html_body(input_string, source_path=None, destination_path=None,
              input_encoding='unicode', doctitle=1, initial_header_level=1):
    """
    Given an input string, returns an HTML fragment as a string.

    The return value is the contents of the <body> element.

    Parameters (see `html_parts()` for the remainder):

    - `output_encoding`: The desired encoding of the output.  If a Unicode
      string is desired, use the default value of "unicode" .
    """
    parts = html_parts(
        input_string=input_string, source_path=source_path,
        destination_path=destination_path,
        input_encoding=input_encoding, doctitle=doctitle,
        initial_header_level=initial_header_level)
    fragment = parts['html_body']
    return fragment

########### Begin: Youtube directive
# this code is used under the MIT license from http://countergram.com/youtube-in-rst
def youtube(name, args, options, content, lineno,
            contentOffset, blockText, state, stateMachine):
    """ Restructured text extension for inserting youtube embedded videos """
    CODE = """\
<object type="application/x-shockwave-flash"
        width="%(width)s"
        height="%(height)s"
        class="youtube-embed"
        data="http://www.youtube.com/v/%(yid)s">
    <param name="movie" value="http://www.youtube.com/v/%(yid)s"></param>
    <param name="wmode" value="transparent"></param>%(extra)s
</object>
"""
    PARAM = """\n    <param name="%s" value="%s"></param>"""

    if len(content) == 0:
        return
    string_vars = {
        'yid': content[0],
        'width': 425,
        'height': 344,
        'extra': ''
        }
    extra_args = content[1:] # Because content[0] is ID
    extra_args = [ea.strip().split("=") for ea in extra_args] # key=value
    extra_args = [ea for ea in extra_args if len(ea) == 2] # drop bad lines
    extra_args = dict(extra_args)
    if 'width' in extra_args:
        string_vars['width'] = extra_args.pop('width')
    if 'height' in extra_args:
        string_vars['height'] = extra_args.pop('height')
    if extra_args:
        params = [PARAM % (key, extra_args[key]) for key in extra_args]
        string_vars['extra'] = "".join(params)
    return [nodes.raw('', CODE % (string_vars), format='html')]

youtube.content = True
directives.register_directive('youtube', youtube)

########### END: Youtube directive


########### Begin: video directive
def videodirective(name, args, options, content, lineno,
            contentOffset, blockText, state, stateMachine):
    """ Restructured text extension for inserting HTML5 embedded videos """
    CODE = """\
<video width="%(width)s" height="%(height)s" controls>
  <source src="%(source)s" type='%(type)s'  />
</video>
"""
  #<source src="test.ogv" type='video/ogg; codecs="theora, vorbis"'>

    if len(content) == 0:
        return
    string_vars = {
        'source': content[0],
        'width': 425,
        'height': 344,
        'type': 'video/webm',
	'codecs': ''
        }

    extra_args = content[1:] # Because content[0] is ID
    extra_args = [ea.strip().split("=") for ea in extra_args] # key=value
    extra_args = [ea for ea in extra_args if len(ea) == 2] # drop bad lines
    extra_args = dict(extra_args)
    if 'width' in extra_args:
        string_vars['width'] = extra_args.pop('width')
    if 'height' in extra_args:
        string_vars['height'] = extra_args.pop('height')
    if 'type' in extra_args:
        string_vars['type'] = extra_args.pop('type')

    return [nodes.raw('', CODE % (string_vars), format='html')]
videodirective.content = True
directives.register_directive('video', videodirective)

########### END: video directive


########### Begin: audio directive
def audiodirective(name, args, options, content, lineno,
            contentOffset, blockText, state, stateMachine):
    """ Restructured text extension for inserting HTML5 embedded audio """
    CODE = """\
<audio controls="controls">
  <source src="%(source)s" type='%(type)s'  />
</audio>
"""

    if len(content) == 0:
        return
    string_vars = {
        'source': content[0],
        'type': 'audio/ogg',
        }

    extra_args = content[1:] # Because content[0] is ID
    extra_args = [ea.strip().split("=") for ea in extra_args] # key=value
    extra_args = [ea for ea in extra_args if len(ea) == 2] # drop bad lines
    extra_args = dict(extra_args)
    if 'type' in extra_args:
        string_vars['type'] = extra_args.pop('type')

    return [nodes.raw('', CODE % (string_vars), format='html')]
audiodirective.content = True
directives.register_directive('audio', audiodirective)

########### END: audio directive

########### Begin: flashvideo directive
def flashvideodirective(name, args, options, content, lineno,
            contentOffset, blockText, state, stateMachine):
    """Restructured text extension for inserting video to be watched with a flash-based video player."""
    CODE = """\
<script type="text/javascript" src="flowplayer-3.2.6.min.js"></script>
<a href="%(source)s" style="display:block;width:%(width)s;height:%(height)s"  id="%(player_id)s"> </a> 
<script> flowplayer("%(player_id)s", "flowplayer-3.2.7.swf", {clip:  { autoPlay: false, autoBuffering: true }}); </script>
"""
    if len(content) == 0:
        return
    string_vars = {
        'source': content[0],
        'width': '',
        'height': '90%',
        'player_id': "player" # TODO: autogen random player id
        }

    extra_args = content[1:] # Because content[0] is ID
    extra_args = [ea.strip().split("=") for ea in extra_args] # key=value
    extra_args = [ea for ea in extra_args if len(ea) == 2] # drop bad lines
    extra_args = dict(extra_args)
    if 'width' in extra_args:
        string_vars['width'] = extra_args.pop('width')
    if 'height' in extra_args:
        string_vars['height'] = extra_args.pop('height')

    return [nodes.raw('', CODE % (string_vars), format='html')]
flashvideodirective.content = True
directives.register_directive('flashvideo', flashvideodirective)

########### END: flashvideo directive
