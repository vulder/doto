#!/bin/bash

pushd() {
  command pushd "$@" > /dev/null
}
popd() {
  command popd "$@" > /dev/null
}

USER=$(whoami)
REPO=$(pwd)

pushd $REPO
git submodule update --init --recursive
popd

ansible-playbook configure_system/main.yml --ask-become-pass \
  --extra-vars "{ 'user':$USER , 'repo':$REPO}"
