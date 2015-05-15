import os
import codecs


EXTENSIONS = {
    'markdown': ['.mdown', '.markdown', '.markdn', '.md', '.mdn', '.mdwn'],
    'restructured_text': ['.rst', '.rest'],
    'textile': ['.textile'],
}


class RenderingError(Exception):
    pass


def render(source):
    ext = os.path.splitext(source)[1]

    # TODO: Support custom encodings
    # TODO: Make codecs open helper?
    text = codecs.open(source, encoding='utf8').read()

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

    # TODO: Is this check needed?
    if text.startswith(u'\ufeff'):  # check for unicode BOM
        text = text[1:]

    return markdown.markdown(text)


def render_restructured_text(text):
    # TODO: Support restructured_text
    pass


def render_textile(text):
    try:
        import textile
    except ImportError:
        raise RenderingError('Could not import `textile` module')

    text = text.replace('\n---\n', '\n<hr />\n')

    return textile.textile(text, encoding='utf8')
