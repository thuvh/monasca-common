#!/bin/bash

set -o xtrace
set -o errexit

pwd

REAL_PATH=$(python -c "import os,sys;print(os.path.realpath('$0'))")
cd "$(dirname "$REAL_PATH")/../docker/"

pwd

docker build --no-cache -t monasca-base:1.0.0 .

docker images
