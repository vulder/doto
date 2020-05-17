#!/bin/bash

eix-sync

emerge -uND --keep-going world

su vulder -c "vi -c 'PlugUpgrade | q'"
su vulder -c "vi -c 'PlugUpdate | qa'"

read -r -p "Update 9999? [y/N] " response
response=${response,,} # tolower
if [[ "$response" =~ ^(yes|y)$ ]]
then
  emerge -1 tig tmux
fi

read -r -p "Build new compiler? [y/N] " response
response=${response,,} # tolower
if [[ "$response" =~ ^(yes|y)$ ]]
then
  echo Building new Compiler
  emerge -1 --keep-going clang clang-common llvm llvm-common compiler-rt compiler-rt-sanitizers llvm-libunwind clang-runtime libcxxabi libcxx libomp mesa lld lldb

  clang++ --version
fi

emerge -a --depclean
