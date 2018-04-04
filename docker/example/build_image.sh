#!/bin/sh
set -x
# This script is used for building Docker image with proper labels.
# To build specific version run this script in the following way:
# $ ./build_image.sh stable/queens

: "${VERSION:=$1}"
[ -z "$VERSION" ] && VERSION=$(grep VERSION Dockerfile | cut -f2 -d"=")

# Image name can be overidden with env var.
: "${DOCKER_IMAGE:=monasca/api}"

[ -z "$REPO_PATH" ] && REPO_PATH=$(grep REPO_PATH Dockerfile | cut -f2 -d"=")
GITHUB_REPO=$(echo "$REPO_PATH" | sed 's/git.openstack.org/github.com/' | \
			  sed 's/ssh:/https:/')

# Clone project to temporary directory for getting proper commit number from
# branches and tags. We need this for setting proper image labels.
# Docker does not allow to get any data from inside of system when building
# image.
TMP_DIR=$(mktemp -d)
git clone "$REPO_PATH" "$TMP_DIR"
cd "$TMP_DIR" || exit 1
GIT_COMMIT=$(git rev-list "$VERSION" --max-count=1)
cd - || exit 1
rm -rf "$TMP_DIR"

# Build-time metadata as defined at
# https://github.com/opencontainers/image-spec/blob/master/annotations.md

docker build --no-cache \
	--build-arg VERSION="$VERSION" \
	--label org.opencontainers.image.created="$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
	--label org.opencontainers.image.url="$GITHUB_REPO" \
	--label org.opencontainers.image.source="$REPO_PATH" \
	--label org.opencontainers.image.version="$VERSION" \
	--label org.opencontainers.image.revision="$GIT_COMMIT" \
	--label org.opencontainers.image.title="$DOCKER_IMAGE" \
	--label org.opencontainers.image.licenses="Apache-2.0" \
	--label org.openstack.constraints_file="" \
	--tag "$DOCKER_IMAGE":"$VERSION" .
