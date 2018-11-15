from setuptools import setup

import landslide

setup(
    name=landslide.__title__,
    version=landslide.__version__,
    description='HTML5 slideshow generator for Markdown, ReST, and Textile',
    packages=['landslide'],
    include_package_data=True,
    zip_safe=False,
    author=landslide.__author__,
    author_email=landslide.__author_email__,
    url='http://github.com/adamzap/landslide',
    license=landslide.__license__,
    platforms=['any'],
    keywords=[
        'markdown',
        'slideshow',
        'presentation',
        'rst',
        'restructuredtext',
        'textile'
    ],
    install_requires=open('requirements.txt').read().strip().split('\n'),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Text Processing :: Markup'
    ],
    long_description='''\
Landslide takes your Markdown, ReST, or Textile file(s) and generates fancy
HTML5 slideshow like `this <http://adamzap.com/misc/presentation.html>`_.

Read the `README <http://github.com/adamzap/landslide/blob/master/README.md>`_
for formatting instructions and more information.
''',
    entry_points={
        'console_scripts': [
            'landslide = landslide.main:main',
        ]
    },
)
