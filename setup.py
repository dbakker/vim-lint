#!/usr/bin/env python

"""Python Distutils setup script for 'vim-lint'."""

from distutils.core import setup

setup(name='vim-lint',
      version='1.0',
      description='Simple linter for Vimscript',
      author='Daan Bakker',
      author_email='bluedaan@gmail.com',
      url='https://github.com/dbakker/vim-lint',
      license='Vim',
      packages=['vimlint'],
      scripts=['scripts/vimlint'],
      package_data={'vimlint': ['data/*.txt']})
