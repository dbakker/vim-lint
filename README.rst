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

Usage
=====

If you'd like to lint your entire `~/.vim` folder::

    find ~/.vim -name *.vim | xargs vimlint | tee out.txt

Enjoy!

License
=======

Copyright (c) Daan Bakker. Distributed under the same terms as Vim itself. See `:help license`.

.. _Syntastic: https://github.com/scrooloose/syntastic
