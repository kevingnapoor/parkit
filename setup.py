#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import Command
import sys


class Tox(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # import here since we just installed it
        import tox
        errno = tox.cmdline([])
        sys.exit(errno)


setup(
    name='parkit',
    version='1.0',
    author='Bryce Lampe',
    description='A small service to show things nearby.',
    packages=['parkit'],
    requires=[
        'flask',
        'flask_scss',
    ],
    tests_require=[
        'tox',
    ],
    cmdclass={'test': Tox},
)
