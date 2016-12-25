#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
## Resources
- [https://packaging.python.org/en/latest/distributing/#readme-rst](https://packaging.python.org/en/latest/distributing/#readme-rst
)
- [http://docs.python-guide.org/en/latest/writing/structure/](http://docs.python-guide.org/en/latest/writing/structure/)
"""

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="tktable",  # name of this project to be listed on PyPI
    version="0.0.1a",  # alpha release
    author="Guilherme Polo",
    author_email="ggpolo@gmail.com",
    maintainer="Nelson Brochado",
    maintainer_email="nelson.brochado@outlook.com",
    description="Wrapper library for Python of the homonymous Tcl/Tk library written by G. Polo",
    long_description=read("README.md"),
    license="The BSD 2-Clause License",
    keywords="table tkinter tcl tk wrapper library",
    url="https://github.com/nbro/tktable",
    include_package_data=True,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Wrapper library",
        "License :: OSI Approved :: The BSD 2-Clause License",
        "Operating System :: MacOS :: Mac OS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    # http://stackoverflow.com/questions/774824/explain-python-entry-points
    entry_points={
        "console_scripts": [
            # type `tktable_demo` on the command line to run a demo
            "tktable_demo = tktable:sample_test"
        ]
    }
)
