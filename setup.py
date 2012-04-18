from setuptools import setup, find_packages

setup(
    name='landslide',
    version='1.0.1',
    description='Lightweight markup language-based html5 slideshow generator',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
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
        'restructuredtext',
        'textile'
    ],
    install_requires=['Jinja2', 'Markdown', 'Pygments', 'docutils'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Text Processing :: Markup'
    ],
    long_description="""\
Landslide takes your Markdown, RST, or Textile file(s) and generates a
slideshow like `this <http://adamzap.com/random/landslide.html>`_.

Read the `README <http://github.com/adamzap/landslide/blob/master/README.md>`_
for formatting instructions and more information.
""",
    entry_points={
        "console_scripts": [
            "landslide = landslide.main:main",
        ]
    },
)
