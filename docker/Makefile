default: docker_build

# Image name can be overidden with env var.
DOCKER_IMAGE ?= monasca/base

# Get actual commit.
# TODO(dobroslaw): This is wrong way, we need commit from inside conatainer.
GIT_COMMIT := $(strip $(shell git rev-parse --short HEAD))

# Prepare tag for image, can be overwritter with env var.
DOCKER_TAG ?= $(GIT_COMMIT)

# Find out if the working directory is clean.
GIT_NOT_CLEAN_CHECK = $(shell git status --porcelain)
ifneq (x$(GIT_NOT_CLEAN_CHECK), x)
DOCKER_TAG_SUFFIX = "-dirty"
endif

docker_build:
	@docker build --no-cache \
		--label org.label-schema.vcs-ref=$(GIT_COMMIT) \
		--label org.label-schema.build-date=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
		--tag $(DOCKER_IMAGE):$(DOCKER_TAG)$(DOCKER_TAG_SUFFIX) .
