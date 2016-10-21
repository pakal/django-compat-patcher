#!/usr/bin/env python

import sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # security

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

classifiers = """\
Development Status :: 1 - Planning
Intended Audience :: Developers
Intended Audience :: Information Technology
Intended Audience :: System Administrators
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Microsoft :: Windows
Operating System :: Unix
Operating System :: MacOS :: MacOS X
"""


setup(
    name='DjangoCompatPatcher',
    version=read("VERSION"),
    author='Pascal Chambon',
    author_email='pythoniks@gmail.com',
    url='https://github.com/pakal/django-compat-patcher',
    license="http://www.opensource.org/licenses/mit-license.php",
    platforms=["any"],
    description="A monkey-patching system to ease the transition between Django versions.",
    classifiers=filter(None, classifiers.split("\n")),
    long_description=read("README.rst"),

    #package_dir={'': 'src'},
    packages=find_packages(),

    # test_suite='your.module.tests',

    use_2to3=True,
    #convert_2to3_doctests=['src/your/module/README.txt'],
    #use_2to3_fixers=['your.fixers'],
    #use_2to3_exclude_fixers=['lib2to3.fixes.fix_import'],
)

