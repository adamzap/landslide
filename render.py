import re
import jinja2
import markdown
import pygments

from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

with open('presentation.html', 'w') as outfile:
    slides_src = markdown.markdown(open('slides.md').read()).split('<hr />\n')

    title = slides_src.pop(0)

    head_title = title.split('>')[1].split('<')[0]

    slides = []

    for slide_src in slides_src:
        header, content = slide_src.split('\n', 1)

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

    template = jinja2.Template(open('base.html').read())

    outfile.write(template.render(locals()))
