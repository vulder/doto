#!/bin/bash

USER=$(whoami)
REPO=$(pwd)

git submodule update --init --recursive

ansible-playbook configure_system/main.yml --ask-become-pass \
  --extra-vars "{ 'user':$USER , 'repo':$REPO}"
