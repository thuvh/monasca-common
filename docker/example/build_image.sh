#!/bin/sh

# TODO(Dobroslaw): move this script to monasca-common/docker folder
# and leave here small script to download it and execute using env variables
# to minimize code duplication.


set -x
# This script is used for building Docker image with proper labels.
# To build specific version run this script in the following way:
# $ ./build_image.sh stable/queens

[ -z "$DOCKER_IMAGE" ] && \
    DOCKER_IMAGE=$(\grep DOCKER_IMAGE Dockerfile | cut -f2 -d"=")

: "${REPO_VERSION:=$1}"
[ -z "$REPO_VERSION" ] && \
    REPO_VERSION=$(\grep REPO_VERSION Dockerfile | cut -f2 -d"=")
REPO_VERSION_CLEAN=$(echo "$REPO_VERSION" | sed 's|/|-|g')

[ -z "$REPO_PATH" ] && REPO_PATH=$(\grep REPO_PATH Dockerfile | cut -f2 -d"=")
GITHUB_REPO=$(echo "$REPO_PATH" | sed 's/git.openstack.org/github.com/' | \
              sed 's/ssh:/https:/')

[ -z "$CONSTRAINTS_BRANCH" ] && \
    CONSTRAINTS_BRANCH=$(\grep CONSTRAINTS_BRANCH Dockerfile | cut -f2 -d"=")
# When using stable version of repository use same stable constraints file.
case "$REPO_VERSION" in
    *stable*)
        CONSTRAINTS_BRANCH_CLEAN=$(echo "$REPO_VERSION" | \
                                   sed 's|origin/||g')
    ;;
    *)
        CONSTRAINTS_BRANCH_CLEAN="$CONSTRAINTS_BRANCH"
    ;;
esac

# Clone project to temporary directory for getting proper commit number from
# branches and tags. We need this for setting proper image labels.
# Docker does not allow to get any data from inside of system when building
# image.
TMP_DIR=$(mktemp -d)
git clone "$REPO_PATH" "$TMP_DIR"
cd "$TMP_DIR" || exit 1
GIT_COMMIT=$(git rev-list "$REPO_VERSION" --max-count=1)
cd - || exit 1
rm -rf "$TMP_DIR"

CREATION_TIME=$(date -u +"%Y%m%dT%H%M%SZ")

docker build --no-cache \
    --build-arg CREATION_TIME="$CREATION_TIME" \
    --build-arg GITHUB_REPO="$GITHUB_REPO" \
    --build-arg REPO_PATH="$REPO_PATH" \
    --build-arg REPO_VERSION="$REPO_VERSION" \
    --build-arg GIT_COMMIT="$GIT_COMMIT" \
    --build-arg CONSTRAINTS_BRANCH="$CONSTRAINTS_BRANCH_CLEAN" \
    --tag "$DOCKER_IMAGE":"$REPO_VERSION_CLEAN" \
    --tag "$DOCKER_IMAGE":"$REPO_VERSION_CLEAN"-"$CREATION_TIME" .
