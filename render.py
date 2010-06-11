#!/usr/bin/env python
import codecs
import re
import jinja2
import markdown
import pygments

from optparse import OptionParser
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

parser = OptionParser()
parser.add_option("-s", "--source", dest="source_file", help="The path to the markdown source file", metavar="FILE", default="slides.md")
parser.add_option("-d", "--destination", dest="target_file", help="The path to the to the destination", metavar="FILE", default="presentation.html")
parser.add_option("-t", "--template", dest="template_file", help="The path to the to the Jinja2 template file", metavar="FILE", default="base.html")

(options, args) = parser.parse_args()

with codecs.open(options.target_file, 'w', encoding='utf8') as outfile:
    slides_src = markdown.markdown(codecs.open(options.source_file, mode='r', encoding='utf8').read()).split('<hr />\n')

    title = slides_src.pop(0)

    head_title = title.split('>')[1].split('<')[0]

    slides = []

    for slide_src in slides_src:
        header, content = slide_src.split('\n', 1)

        while '<code>!' in content:
            lang_match = re.search('<code>!(.+)\n', content)

            if lang_match:
                lang = lang_match.group(1)
                code = content.split(lang, 1)[1].split('</code', 1)[0]

                lexer = get_lexer_by_name(lang)

                formatter = HtmlFormatter(linenos='inline', noclasses=True,
                                          nobackground=True)

                pretty_code = pygments.highlight(code, lexer, formatter)
                pretty_code = pretty_code.replace('&amp;', '&')

                before_code = content.split('<code>', 1)[0]
                after_code = content.split('</code>', 1)[1]

                content = before_code + pretty_code + after_code

        slides.append({'header': header, 'content': content})

    template = jinja2.Template(open(options.template_file).read())

    outfile.write(template.render(locals()))

print "Generated %s" % options.target_file