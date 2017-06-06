#!/bin/bash

eix-sync

emerge -auND --keep-going world

su vulder -c "vi -c 'PlugUpgrade | q'"
su vulder -c "vi -c 'PlugUpdate | qa'"

read -r -p "Update 9999? [y/N] " response
response=${response,,} # tolower
if [[ "$response" =~ ^(yes|y)$ ]]
then
  emerge -a1 neovim tig llvm-vim
fi

read -r -p "Build new compiler? [y/N] " response
response=${response,,} # tolower
if [[ "$response" =~ ^(yes|y)$ ]]
then
  echo Building new Compiler
  emerge -a1 --keep-going clang llvm compiler-rt compiler-rt-sanitizers llvm-libunwind clang-runtime libcxxabi libcxx libomp mesa

  clang++ --version; clang_old++ --version

  read -r -p "Install new compiler? [y/N] " response
  response=${response,,} # tolower
  if [[ "$response" =~ ^(yes|y)$ ]]
  then
    echo Updating clang
    cp -r /usr/lib/llvm/5/* /usr/lib/llvm/5_old/
  fi
fi

