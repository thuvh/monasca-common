#!/bin/bash

set -o xtrace
set -o errexit

REAL_PATH=$(python -c "import os,sys;print(os.path.realpath('$0'))")
cd "$(dirname "$REAL_PATH")/../docker/"

CREATION_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
# Docker tags don't like colons so use shorter version of ISO 8601 for them.
CREATION_TIME_SHORT=$(date -d "$CREATION_TIME" -u +"%Y%m%dT%H%M%SZ")

docker build --no-cache \
    --tag monasca-base:latest \
    --tag monasca-base:"$CREATION_TIME_SHORT" .

docker images
