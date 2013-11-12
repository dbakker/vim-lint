if exists('g:loaded_syntastic_vim_vimlint_checker')
  finish
endif
let g:loaded_syntastic_vim_vimlint_checker = 1

function! s:get_vimlint()
    if !exists('s:vimlint_exe')
        let paths = substitute(escape(&runtimepath, ' '), '\(,\|$\)', '/**\1', 'g')
        let s:vimlint_exe = fnamemodify(findfile('vimlint.py', paths), ':p')
    endif
    return s:vimlint_exe
endfunction

function! SyntaxCheckers_vim_vimlint_IsAvailable() dict
  return executable('python') && filereadable(s:get_vimlint())
endfunction

let s:save_cpo = &cpo
set cpo&vim

function! SyntaxCheckers_vim_vimlint_GetLocList() dict
  let python = executable('python2') ? 'python2' : 'python'

  let makeprg = self.makeprgBuild({
        \ 'exe': python.' '.s:get_vimlint(),
        \ 'filetype': 'vim',
        \ 'subchecker': 'vimlint' })

  let errorformat =
        \ '%f:%l:%c: %trror: %m,' .
        \ '%f:%l:%c: %tarning: %m'

  " process makeprg
  let errors = SyntasticMake({ 'makeprg': makeprg,
        \ 'errorformat': errorformat })

  return errors
endfunction

call g:SyntasticRegistry.CreateAndRegisterChecker({
      \ 'filetype': 'vim',
      \ 'name': 'vimlint'})

let &cpo = s:save_cpo
unlet s:save_cpo

" vim: set et sts=4 sw=4:
