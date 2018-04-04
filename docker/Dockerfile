FROM python:3.5.5-alpine3.7

COPY wait_for.sh kafka_wait_for_topics.py /
COPY ashrc /root/.ashrc

ENV \
    ENV="/root/.ashrc" \
    PIP_FORCE_REINSTALL="true" \
    PIP_NO_CACHE_DIR="no" \
    PIP_NO_COMPILE="no" \
    PYTHONIOENCODING="utf-8"

RUN \
    chmod +x /wait_for.sh /kafka_wait_for_topics.py && \
    apk add --no-cache \
        ca-certificates=20171114-r0 \
        su-exec=0.2-r0 \
        tini=0.16.1-r0 \
        tzdata=2017c-r0 && \
    pip3 install \
        pykafka==2.7.0 \
        PyMySQL===0.8.1 \
        Templer==1.1.4 && \
    rm -rf /var/cache/apk/* && \
    rm -rf /tmp/* && \
    rm -rf /var/log/*

# Get values from child images
ONBUILD ARG CREATION_TIME
ONBUILD ARG DOCKER_IMAGE
ONBUILD ARG REPO_PATH
ONBUILD ARG GITHUB_REPO
ONBUILD ARG REPO_VERSION
ONBUILD ARG GIT_COMMIT
ONBUILD ARG CONSTRAINTS_BRANCH
ONBUILD ARG CONSTRAINTS_PATH=http://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt
ONBUILD ARG EXTRA_DEPS

# Build-time metadata as defined at
# https://github.com/opencontainers/image-spec/blob/master/annotations.md
ONBUILD LABEL org.opencontainers.image.created="$CREATION_TIME"
ONBUILD LABEL org.opencontainers.image.title="$DOCKER_IMAGE"
ONBUILD LABEL org.opencontainers.image.source="$REPO_PATH"
ONBUILD LABEL org.opencontainers.image.url="$GITHUB_REPO"
ONBUILD LABEL org.opencontainers.image.version="$REPO_VERSION"
ONBUILD LABEL org.opencontainers.image.revision="$GIT_COMMIT"
ONBUILD LABEL org.opencontainers.image.licenses="Apache-2.0"
ONBUILD LABEL org.openstack.constraints_uri="$CONSTRAINTS_PATH?h=$CONSTRAINTS_BRANCH"
ONBUILD LABEL org.openstack.monasca.python.extra_deps="$EXTRA_DEPS"

# Every child image need to provide starting and health check script.
# If they're not provided build will fail. We want that for uniformity.
ONBUILD COPY start.sh health_check.py /

ONBUILD WORKDIR /

ONBUILD RUN \
            chmod +x /start.sh && \
            apk add --no-cache --virtual .build-deps \
                g++=6.4.0-r5 \
                git=2.15.2-r0 \
                linux-headers=4.4.6-r2 \
                make=4.2.1-r0 && \
            # Clone repository and checkout requested version.
            git clone $REPO_PATH /app && \
            git -C /app reset --hard $REPO_VERSION && \
            # Install our application with extra dependencies if provided.
            # BUG(Dobroslaw): pip install also all test dependencies
            pip3 install \
                /app/. $EXTRA_DEPS \
                --requirement /app/requirements.txt \
                --constraint $CONSTRAINTS_PATH?h=$CONSTRAINTS_BRANCH && \
            # Save info about build to `/VERSIONS` file.
            printf "Repository: %s\n" $REPO_PATH >> /VERSIONS && \
            printf "Version: %s\n" $REPO_VERSION >> /VERSIONS && \
            printf "Revision: %s\n" `git rev-parse HEAD` >> /VERSIONS && \
            printf "Constraints file: %s\n" $CONSTRAINTS_PATH?h=$CONSTRAINTS_BRANCH >> /VERSIONS && \
            # Clean after instalation.
            apk del .build-deps && \
            rm -rf /var/cache/apk/* && \
            rm -rf /tmp/* && \
            rm -rf /var/log/* && \
            rm -rf /app

ONBUILD HEALTHCHECK --interval=5m --timeout=3s \
                   CMD python3 health_check.py || exit 1

ENTRYPOINT ["/sbin/tini", "-s", "--"]
