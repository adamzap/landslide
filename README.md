html5-slides-markdown
=====================

Generates a slideshow using the slides that power
[the html5-slides presentation](http://apirocks.com/html5/html5.html).

A sample slideshow is [here](http://adamzap.com/random/html5-slides-markdown.html).

A `python` with the `jinja2`, `markdown`, and `pygments` modules is required.

Markdown Formatting Instructions
--------------------------------

- Separate your slides with a horizontal rule (--- in markdown)
- Your first slide (title slide) should not have a heading, only `<p>`s
- Your other slides should have a heading that renders to an h1 element
- To highlight blocks of code, put !{{lang}} as the first indented line
- See the included slides.md for an example

Rendering Instructions
----------------------

- Put your markdown content in a file called `slides.md`
- Run `python render.py`
- Enjoy your newly generated `presentation.html`

TODO
----

- Test CSS for all Markdown features
- Highlight syntax for more than one code block per page

Thanks
------

- bradcupit (for suggestions and encouragement)
