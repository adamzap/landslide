from distutils.core import setup

setup(
    name='landslide',
    packages=['landslide'],
    package_data={'landslide': [
        'themes/default/*.html',
        'themes/default/css/*.css',
        'themes/default/js/*.js']},
    version='0.6.0',
    description='Lightweight markup language-based html5 slideshow generator',
    author='Adam Zapletal',
    author_email='adamzap@gmail.com',
    url='http://github.com/adamzap/landslide',
    license='Apache 2.0',
    platforms=['any'],
    keywords=[
        'markdown',
        'slideshow',
        'presentation',
        'rst',
        'restructuredtext'
    ],
    requires=['Jinja2', 'Markdown', 'Pygments', 'docutils'],
    scripts=['landslide/landslide'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Text Processing :: Markup'
    ],
    long_description="""\
Landslide takes your Markdown or RST file(s) and generates a slideshow like
`this <http://adamzap.com/random/landslide.html>`_.

Read the `README <http://github.com/adamzap/landslide/blob/master/README.md>`_
for formatting instructions and more information.
""")
