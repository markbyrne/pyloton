#! /usr/bin/env python3.9
# -*- coding: latin-1 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='pyloton',
    version='0.1.0',
    author='Mark Byrne',
    author_email='MarkByrne2015@gmail.com',
    packages=setuptools.find_packages(),
    scripts=[],
    url='https://github.com/markbyrne/pyloton',
    license='LICENSE.txt',
    description='Peloton API Python Integration',
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0-only",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "json",
        "os"
    ],
)
