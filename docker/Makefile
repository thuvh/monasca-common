default: docker_build

# Image name can be overidden with env var.
DOCKER_IMAGE ?= monasca/base

# Get actual commit.
# TODO(dobroslaw): This is wrong way, we need commit from inside the container.
GIT_COMMIT := $(strip $(shell git rev-parse --short HEAD))

# Prepare tag for image, can be overwritter with env var.
DOCKER_TAG ?= $(GIT_COMMIT)

# Find out if the working directory is clean.
GIT_NOT_CLEAN_CHECK = $(shell git status --porcelain)
ifneq (x$(GIT_NOT_CLEAN_CHECK), x)
DOCKER_TAG_SUFFIX = "-dirty"
endif

# Build-time metadata as defined at
# https://github.com/opencontainers/image-spec/blob/master/annotations.md
# TODO(dobroslaw): version should be only added when building from clean
# branch or tag. Ommit for specific commit or add `-dirty` to version.

docker_build:
	@docker build --no-cache \
		--label org.opencontainers.image.created=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
		--label org.opencontainers.image.url="https://github.com/openstack/monasca-common" \
		--label org.opencontainers.image.source="https://git.openstack.org/cgit/openstack/monasca-common" \
		--label org.opencontainers.image.version="1.2.3" \
		--label org.opencontainers.image.revision=$(GIT_COMMIT) \
		--label org.opencontainers.image.title="monasca-base" \
		--label org.opencontainers.image.licenses="Apache-2.0" \
		--tag $(DOCKER_IMAGE):$(DOCKER_TAG)$(DOCKER_TAG_SUFFIX) .
