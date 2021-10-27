#!/bin/bash

pushd() {
  command pushd "$@" > /dev/null
}
popd() {
  command popd "$@" > /dev/null
}

USER=$(whoami)
REPO=$(pwd)
HOST=`/bin/hostname --short`

pushd $REPO
git submodule update --init --recursive

ansible-playbook -i "configure_system/hosts" \
  --connection=local \
  --limit="${HOST}" \
  --ask-become-pass \
  --extra-vars "{ 'user':$USER , 'repo':$REPO }" \
  configure_system/main.yml

popd
