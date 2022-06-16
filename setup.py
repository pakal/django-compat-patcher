#!/usr/bin/env python

import sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # security

from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def read_file(fname):
    if not os.path.isabs(fname):
        fname = os.path.join(ROOT_DIR, fname)
    return open(os.path.join(os.path.dirname(__file__), fname)).read().strip()

VERSION = read_file("VERSION").strip()

assert VERSION == "0.11", VERSION  # ELSE CHECK THESE PYTHON VERSION CLASSIFIERS BELOW FOR UPDATES
classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: Information Technology
License :: OSI Approved :: MIT License
Natural Language :: English
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Microsoft :: Windows
Operating System :: Unix
Operating System :: MacOS :: MacOS X
"""

packages = find_packages(where="src")

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
setup_requires = ["pytest-runner"] if needs_pytest else []

extras = {"comments": ["django-contrib-comments"]}

setup(
    name="django-compat-patcher",
    version=VERSION,
    author="Pascal Chambon & others",
    author_email="pythoniks@gmail.com",
    url="https://github.com/pakal/django-compat-patcher",
    license="MIT",
    platforms=["any"],
    description="A monkey-patcher to ease the transition of project to latest Django versions.",
    classifiers=filter(None, classifiers.split("\n")),
    long_description=read_file("README.rst"),
    package_dir={"": "src"},
    packages=packages,
    install_requires=['compat-patcher-core>=1.2',
                      'six',
                      'Django<2;python_version<"3.0"',
                      'Django;python_version>="3.0"'],
    extras_require=extras,
    setup_requires=setup_requires,
    tests_require=[
        "pytest",
        "pytest-cov",
        "django-compat",
    ],  # Beware, keep in sync with tox.ini
)
