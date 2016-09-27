import os
import re
import codecs


EXTENSIONS = {
    'markdown': ['.mdown', '.markdown', '.markdn', '.md', '.mdn', '.mdwn'],
    'restructured_text': ['.rst', '.rest'],
    'textile': ['.textile'],
}


MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite'
]


class RenderingError(Exception):
    pass


def render(source):
    ext = os.path.splitext(source)[1]

    # TODO: Support custom encodings
    # TODO: Make codecs open helper?
    text = codecs.open(source, encoding='utf8').read()

    text = text.lstrip(unicode(codecs.BOM_UTF8, 'utf8'))

    if ext in EXTENSIONS['markdown']:
        return render_markdown(text)
    elif ext in EXTENSIONS['restructured_text']:
        return render_restructured_text(text)
    elif ext in EXTENSIONS['textile']:
        return render_textile(text)
    else:
        raise RenderingError('Unsupported file extension: %s' % source)


def render_markdown(text):
    # TODO: Support markdown extensions
    try:
        import markdown
    except ImportError:
        raise RenderingError('Could not import `markdown` module')

    return markdown.markdown(text, extensions=MARKDOWN_EXTENSIONS)


def render_restructured_text(text):
    try:
        from docutils.core import publish_string
    except ImportError:
        raise RenderingError('Could not import `docutils` module')

    import rst_pygments

    opts = {
        'embed_stylesheet': False,
        'report_level': 5
    }

    html = publish_string(text, writer_name='html', settings_overrides=opts)

    html = html.split('\n\n\n', 1)[1]
    html = html.split('</div>\n</body>\n</html>')[0]
    html = html.replace(' class="docutils"', '')
    html = re.sub('<div class="section"(.+)?>\n', '', html)
    html = html.replace('</div>\n', '')
    html = html.replace('\n\n', '\n')

    return html


def render_textile(text):
    try:
        import textile
    except ImportError:
        raise RenderingError('Could not import `textile` module')

    text = text.replace('\n---\n', '\n<hr />\n')

    return textile.textile(text, encoding='utf8')
