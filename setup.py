#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import sys

from setuptools import setup, find_packages


def read_file(fname):
    """
    Read file and decode in py2k
    """
    if sys.version_info < (3,):
        return open(fname).read().decode("utf-8")
    return open(fname).read()


dist_name = 'kolibri_pratham_plugin'
plugin_name = 'kolibri_pratham_plugin'
repo_url = 'https://github.com/learningequality/kolibri-pratham-plugin.git'

readme = read_file('README.rst')
doclink = """
Documentation
-------------

The full documentation is at."""

# Default description of the distributed package
description = (
    """Kolibri Plugin to provide specific functionality for integration needs for Pratham"""
)


######################################
# STATIC AND DYNAMIC BUILD SPECIFICS #
######################################

def enable_log_to_stdout(logname):
    """Given a log name, outputs > INFO to stdout."""
    log = logging.getLogger(logname)
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    log.addHandler(ch)


setup(
    name=dist_name,
    version="0.1",
    description=description,
    long_description="{readme}\n\n{doclink}".format(
        readme=readme,
        doclink=doclink
    ),
    author='Learning Equality',
    author_email='info@learningequality.org',
    url=repo_url,
    packages=find_packages(),
    package_dir={plugin_name: plugin_name},
    install_requires=[],
    include_package_data=True,
    license='All Rights Reserved',
    zip_safe=False,
    keywords='kolibri',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
