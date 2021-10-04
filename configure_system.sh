#!/bin/bash

USER=$(whoami)
REPO=$(pwd)

ansible-playbook configure_system/main.yml --ask-become-pass \
  --extra-vars "{ 'user':$USER , 'repo':$REPO}"
