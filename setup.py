from distutils.core import setup

setup(
    name = 'landslide',
    packages = ['landslide'],
    package_data = {'landslide': ['templates/*']},
    version = '0.4.0',
    description = 'Markdown-based html5 slideshow generator',
    author = 'Adam Zapletal',
    author_email = 'adamzap@gmail.com',
    url = 'http://github.com/adamzap/landslide',
    license = 'Apache 2.0',
    platforms = ['any'],
    keywords = ['markdown', 'slideshow', 'presentation'],
    requires = ['Markdown', 'Jinja2', 'Pygments'],
    scripts = ['landslide/landslide'],
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Text Processing :: Markup'
    ],
    long_description = """\
Landslide takes your Markdown file(s) and generates a slideshow like
`this <http://adamzap.com/random/landslide.html>`_.

Read the `README <http://github.com/adamzap/landslide/blob/master/README.md>`_
for formatting instructions and more information.
"""
)
