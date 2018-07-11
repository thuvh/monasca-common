#!/bin/bash

set -o xtrace
set -o errexit

docker build --no-cache -t monasca-base:1.0.0 .

docker images
