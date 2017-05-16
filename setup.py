"""
simpleparallel Copyright (C) 2016  Steven Cutting
"""

from setuptools import setup, find_packages
try:
    with open("README.md") as fp:
        THE_LONG_DESCRIPTION = fp.read()
except IOError:
    THE_LONG_DESCRIPTION = ''

setup(
    name="simpleparallel",
    url="https://github.com/steven-cutting/simpleparallel",
    # Semantic versioning. MAJOR.MINOR.MAINTENANCE.(dev1|a1|b1)
    version="0.0.0.dev1",
    license='GNU GPL v3+',

    description="",
    long_description=THE_LONG_DESCRIPTION,

    author='Steven Cutting',
    author_email='steven.e.cutting@linux.com',

    classifiers=['Operating System :: OS Independent',
                 'Development Status :: 3 - Alpha',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Development Status :: 2 - Pre-Alpha',
                 ],
    keywords='nlp text ngram ngrams',
    packages=find_packages(exclude=('bin', 'tests', 'docker',
                                    'data', 'notebooks')),
    # scripts=['bin/word-counts', 'bin/text-2-bow'],
    install_requires=['toolz>=0.8.2',
                      ],
    extras_require={
        'faster': ['cytoolz>=0.8.2'],
        'dev': ['cytoolz>=0.8.2'],
        'test': ['pytest-runner>=2.6.2', 'pytest>=2.8.7'],
    },
    setup_requires=['pytest-runner>=2.6.2'],
    tests_require=['pytest>=2.8.7'],
    )
