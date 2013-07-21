Vim Lint
========

VimLint is, you guessed it, a sourcecode checker for your `.vimrc` (and
all other Vimscript)! It finds common problems such as:

* Trying to use (ex-)commands that do not exist
* Missing the `if` or `endif` in `if...endif`.
* Incorrectly using options, f.e. `set compatible=3` would be incorrect as only
  `set compatible` and `set nocompatible` are allowed.
* Incorrect syntax for mappings.
* And many more...

It works together with Syntastic_, which is an amazing Vim plugin that uses
external source code checkers to find and highlight errors.

All the cool kids are using it, and so should you!

Installing
----------

Installing vim-lint is really easy! Make sure you have `python` in your PATH,
Syntastic_ installed and add vim-lint to your bundles:

For Vundle_ you just need to make sure you have the following 2 lines in your `.vimrc`::

    Bundle 'scrooloose/syntastic'
    Bundle 'dbakker/vim-lint'

For Pathogen_, execute::

    cd ~/.vim/bundle
    git clone https://github.com/dbakker/vim-lint.git
    git clone https://github.com/scrooloose/syntastic.git
    vim +Helptags +q

Usage
=====

Check out the documentation that comes with Syntastic (`:h syntastic`) to see what you can do. If you'd like
to lint your entire `~/.vim` folder, you can use VimLint like a standalone utility::

    find ~/.vim -name *.vim|xargs python ~/.vim/bundle/vim-lint/vimlint/vimlint.py > out.txt

Enjoy!

License
=======

Copyright (c) Daan Bakker. Distributed under the same terms as Vim itself. See `:help license`.

.. _Vundle: https://github.com/gmarik/vundle
.. _Pathogen: https://github.com/tpope/vim-pathogen
.. _Syntastic: https://github.com/scrooloose/syntastic
