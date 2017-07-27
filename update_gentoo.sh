#!/bin/bash

eix-sync

emerge -uND --keep-going world

su vulder -c "vi -c 'PlugUpgrade | q'"
su vulder -c "vi -c 'PlugUpdate | qa'"

read -r -p "Update 9999? [y/N] " response
response=${response,,} # tolower
if [[ "$response" =~ ^(yes|y)$ ]]
then
  emerge -1 neovim tig llvm-common
fi

read -r -p "Build new compiler? [y/N] " response
response=${response,,} # tolower
if [[ "$response" =~ ^(yes|y)$ ]]
then
  echo Building new Compiler
  emerge -1 --keep-going clang llvm compiler-rt compiler-rt-sanitizers llvm-libunwind clang-runtime libcxxabi libcxx libomp mesa

  clang++ --version; clang_old++ --version

  read -r -p "Install new compiler? [y/N] " response
  response=${response,,} # tolower
  if [[ "$response" =~ ^(yes|y)$ ]]
  then
    echo Updating clang
    cp -r /usr/lib/llvm/6/* /usr/lib/llvm/6_old/
  fi
fi

