#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import re

from setuptools import setup, find_packages


def get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, 'rb') as f:
            return f.read().decode('utf8')
    except IOError:
        pass


def get_version():
    init_py = get_file(os.path.dirname(__file__), 'idioma', '__init__.py')
    pattern = r"{0}\W*=\W*'([^']+)'".format('__version__')
    version, = re.findall(pattern, init_py)
    return version


def get_description():
    init_py = get_file(os.path.dirname(__file__), 'idioma', '__init__.py')
    pattern = r'"""(.*?)"""'
    description, = re.findall(pattern, init_py, re.DOTALL)
    return description


def get_readme():
    return get_file(os.path.dirname(__file__), 'README.rst')


tests_requires = [
    'pytest',
    'flake8',
]

install_requires = [
    'httpx~=0.25.0',
]


def install():
    setup(
        name='idioma',
        version=get_version(),
        description=get_description(),
        long_description=get_readme(),
        license='MIT',
        author='SuHun Han',
        author_email='ssut' '@' 'ssut.me',
        url='https://github.com/ssut/py-idioma',
        classifiers=['Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Education',
                     'Intended Audience :: End Users/Desktop',
                     'License :: Freeware',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Education',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3.8'],
        packages=find_packages(exclude=['docs', 'tests']),
        keywords='google translate translator',
        install_requires=install_requires,
        python_requires='>=3.8',
        tests_require=tests_requires,
        extras_require={
            "tests": install_requires + tests_requires
        },
        scripts=['translate']
    )


if __name__ == "__main__":
    install()
