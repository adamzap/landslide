# -*- coding: utf-8 -*-

import os
import re
import unittest

from generator import Generator


SAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'samples')
if (not os.path.exists(SAMPLES_DIR)):
    raise IOError('Sample source files not found, cannot run tests')


class WarningMessage(Exception):
    pass


class ErrorMessage(Exception):
    pass


class GeneratorTest(unittest.TestCase):
    def logtest(self, message, type):
        if type == 'warning':
            raise WarningMessage(message)
        elif type == 'error':
            raise ErrorMessage(message)

    def test___init__(self):
        self.assertRaises(IOError, Generator, None)
        self.assertRaises(IOError, Generator, 'foo.md')

    def test_embed_images(self):
        base_dir = os.path.join(SAMPLES_DIR, 'example1', 'slides.md')
        g = Generator(base_dir, logger=self.logtest)
        self.assertRaises(WarningMessage, g.embed_images,
                          '<img src="toto.jpg"/>', '.')
        content = g.embed_images('<img src="monkey.jpg"/>', base_dir)
        self.assertTrue(re.match('<img src="data:image/jpeg;base64,(.+?)"/>',
                        content))

    def test_get_slide_vars(self):
        g = Generator(os.path.join(SAMPLES_DIR, 'example1', 'slides.md'))
        vars = g.get_slide_vars("<h1>heading</h1>\n<p>foo</p>\n<p>bar</p>\n")
        self.assertEqual(vars['header'], '<h1>heading</h1>')
        self.assertEqual(vars['content'], '<p>foo</p>\n<p>bar</p>')

    def test_get_template_vars(self):
        g = Generator(os.path.join(SAMPLES_DIR, 'example1', 'slides.md'))
        vars = g.get_template_vars(["<h1>slide1</h1>\n<p>content1</p>",
                                    "<h1>slide2</h1>\n<p>content2</p>",
                                    "<p>no heading here</p>"])
        self.assertEqual(vars['head_title'], 'slide1')
        slides = vars['slides']
        self.assertEqual(slides[0]['header'], '<h1>slide1</h1>')
        self.assertEqual(slides[0]['content'], '<p>content1</p>')
        self.assertEqual(slides[1]['header'], '<h1>slide2</h1>')
        self.assertEqual(slides[1]['content'], '<p>content2</p>')
        self.assertEqual(slides[2]['header'], None)
        self.assertEqual(slides[2]['content'], '<p>no heading here</p>')

    def test_highlight_code(self):
        g = Generator(os.path.join(SAMPLES_DIR, 'example1', 'slides.md'))
        hl = g.highlight_code("<pre><code>!php\n$foo;</code></pre>")
        self.assertTrue(hl.startswith('<pre><div class="highlight">'))
        input = "<p>Nothing to declare</p>"
        self.assertEqual(g.highlight_code(input), input)

if __name__ == '__main__':
    unittest.main()
