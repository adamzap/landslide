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
import unittest

from generator import Generator
from macro import *
from parser import Parser


SAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'samples')
if (not os.path.exists(SAMPLES_DIR)):
    raise IOError('Sample source files not found, cannot run tests')


class BaseTestCase(unittest.TestCase):
    def logtest(self, message, type='notice'):
        if type == 'warning':
            raise WarningMessage(message)
        elif type == 'error':
            raise ErrorMessage(message)


class GeneratorTest(BaseTestCase):
    def test___init__(self):
        self.assertRaises(IOError, Generator, None)
        self.assertRaises(IOError, Generator, 'foo.md')

    def test_get_toc(self):
        base_dir = os.path.join(SAMPLES_DIR, 'example1', 'slides.md')
        g = Generator(base_dir, logger=self.logtest)
        g.add_toc_entry('Section 1', 1, 1)
        g.add_toc_entry('Section 1.1', 2, 2)
        g.add_toc_entry('Section 1.2', 2, 3)
        g.add_toc_entry('Section 2', 1, 4)
        g.add_toc_entry('Section 2.1', 2, 5)
        g.add_toc_entry('Section 3', 1, 6)
        toc = g.toc
        self.assertEqual(len(toc), 3)
        self.assertEqual(toc[0]['title'], 'Section 1')
        self.assertEqual(len(toc[0]['sub']), 2)
        self.assertEqual(toc[0]['sub'][1]['title'], 'Section 1.2')
        self.assertEqual(toc[1]['title'], 'Section 2')
        self.assertEqual(len(toc[1]['sub']), 1)
        self.assertEqual(toc[2]['title'], 'Section 3')
        self.assertEqual(len(toc[2]['sub']), 0)

    def test_get_slide_vars(self):
        g = Generator(os.path.join(SAMPLES_DIR, 'example1', 'slides.md'))
        svars = g.get_slide_vars("<h1>heading</h1>\n<p>foo</p>\n<p>bar</p>\n")
        self.assertEqual(svars['title'], 'heading')
        self.assertEqual(svars['level'], 1)
        self.assertEqual(svars['header'], '<h1>heading</h1>')
        self.assertEqual(svars['content'], '<p>foo</p>\n<p>bar</p>')
        self.assertEqual(svars['source'], {})
        self.assertEqual(svars['classes'], [])

    def test_unicode(self):
        g = Generator(os.path.join(SAMPLES_DIR, 'example3', 'slides.rst'))
        g.execute()

    def test_get_template_vars(self):
        g = Generator(os.path.join(SAMPLES_DIR, 'example1', 'slides.md'))
        svars = g.get_template_vars([{'title': "slide1", 'level': 1},
                                     {'title': "slide2", 'level': 1},
                                     {'title': None, 'level': 1},
                                    ])
        self.assertEqual(svars['head_title'], 'slide1')

    def test_process_macros(self):
        g = Generator(os.path.join(SAMPLES_DIR, 'example1', 'slides.md'))
        # Notes
        r = g.process_macros('<p>foo</p>\n<p>.notes: bar</p>\n<p>baz</p>')
        self.assertEqual(r[0].find('<p class="notes">bar</p>'), 11)
        self.assertEqual(r[1], [u'has_notes'])
        # FXs
        content = '<p>foo</p>\n<p>.fx: blah blob</p>\n<p>baz</p>'
        r = g.process_macros(content)
        self.assertEqual(r[0], '<p>foo</p>\n<p>baz</p>')
        self.assertEqual(r[1][0], 'blah')
        self.assertEqual(r[1][1], 'blob')

    def test_register_macro(self):
        g = Generator(os.path.join(SAMPLES_DIR, 'example1', 'slides.md'))

        class SampleMacro(Macro):
            pass

        g.register_macro(SampleMacro)
        self.assertTrue(SampleMacro in g.macros)

        def plop(foo):
            pass

        self.assertRaises(TypeError, g.register_macro, plop)


class CodeHighlightingMacroTest(BaseTestCase):
    def test_descape(self):
        m = CodeHighlightingMacro(self.logtest)
        self.assertEqual(m.descape('foo'), 'foo')
        self.assertEqual(m.descape('&gt;'), '>')
        self.assertEqual(m.descape('&lt;'), '<')
        self.assertEqual(m.descape('&amp;lt;'), '&lt;')
        self.assertEqual(m.descape('&lt;span&gt;'), '<span>')
        self.assertEqual(m.descape('&lt;spam&amp;eggs&gt;'), '<spam&eggs>')

    def test_process(self):
        m = CodeHighlightingMacro(self.logtest)
        hl = m.process("<pre><code>!php\n$foo;</code></pre>")
        self.assertTrue(hl[0].startswith('<div class="highlight"><pre'))
        self.assertTrue(hl[1], 'code')
        input = "<p>Nothing to declare</p>"
        self.assertEqual(m.process(input)[0], input)
        self.assertEqual(m.process(input)[1], [])


class EmbedImagesMacroTest(BaseTestCase):
    def test_process(self):
        base_dir = os.path.join(SAMPLES_DIR, 'example1', 'slides.md')
        m = EmbedImagesMacro(self.logtest, True)
        self.assertRaises(WarningMessage, m.process,
                          '<img src="toto.jpg"/>', '.')
        content, classes = m.process('<img src="monkey.jpg"/>', base_dir)
        self.assertTrue(re.match(r'<img src="data:image/jpeg;base64,(.+?)"/>',
                        content))


class FixImagePathsMacroTest(BaseTestCase):
    def test_process(self):
        base_dir = os.path.join(SAMPLES_DIR, 'example1', 'slides.md')
        m = FixImagePathsMacro(self.logtest, False)
        content, classes = m.process('<img src="monkey.jpg"/>', base_dir)
        self.assertTrue(re.match(r'<img src="file://.*?/monkey.jpg" />',
                                 content))


class FxMacroTest(BaseTestCase):
    def test_process(self):
        m = FxMacro(self.logtest)
        content = '<p>foo</p>\n<p>.fx: blah blob</p>\n<p>baz</p>'
        r = m.process(content)
        self.assertEqual(r[0], '<p>foo</p>\n<p>baz</p>')
        self.assertEqual(r[1][0], 'blah')
        self.assertEqual(r[1][1], 'blob')


class NotesMacroTest(BaseTestCase):
    def test_process(self):
        m = NotesMacro(self.logtest)
        r = m.process('<p>foo</p>\n<p>.notes: bar</p>\n<p>baz</p>')
        self.assertEqual(r[0].find('<p class="notes">bar</p>'), 11)
        self.assertEqual(r[1], [u'has_notes'])


class ParserTest(BaseTestCase):
    def test___init__(self):
        self.assertEqual(Parser('.md').format, 'markdown')
        self.assertEqual(Parser('.markdown').format, 'markdown')
        self.assertEqual(Parser('.rst').format, 'restructuredtext')
        self.assertRaises(NotImplementedError, Parser, '.txt')


class WarningMessage(Exception):
    pass


class ErrorMessage(Exception):
    pass

if __name__ == '__main__':
    unittest.main()
