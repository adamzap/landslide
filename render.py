import jinja2
import markdown

with open('presentation.html', 'w') as outfile:
    slides_src = markdown.markdown(open('slides.md').read()).split('<hr />\n')

    title = slides_src.pop(0)

    slides = []

    for slide_src in slides_src:
        header, content = slide_src.split('\n', 1)
        slides.append({'header': header, 'content': content})

    template = jinja2.Template(open('base.html').read())

    outfile.write(template.render({'title': title, 'slides': slides}))
