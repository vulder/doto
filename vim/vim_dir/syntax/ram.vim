" Vim syntax file
" Language:   RAM
" Maintainer: Florian Sattler
" Version:      $Revision: 1 $

if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

syn case match

syn keyword arith add add@ addAbs
syn keyword arith sub sub@ subAbs
syn keyword arith mult mult@ multAbs

syn keyword L load load@ loadAbs
syn keyword S store store@ storeAbs

syn keyword jp jumpGtz jumpGtz@ jumpGtzAbs jumpZ jumpZ@ jumpZAbs

syn keyword IO read print

syn match loopmarker "<-"
syn match loopmarker "->"

syn match ramComment /\/\/.*$/

if version >= 508 || !exists("did_c_syn_inits")
  if version < 508
    let did_c_syn_inits = 1
    command -nargs=+ HiLink hi link <args>
  else
    command -nargs=+ HiLink hi def link <args>
  endif

  HiLink arith Type
  HiLink L Statement
  HiLink S Boolean
  HiLink jp String
  HiLink IO Identifier
  HiLink ramComment Comment
  HiLink loopmarker Directory

  delcommand HiLink
endif

let b:current_syntax = "ram"
