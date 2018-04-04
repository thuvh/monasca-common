FROM python:3.5.5-alpine3.7

COPY wait_for.sh kafka_wait_for_topics.py /
COPY ashrc /root/.ashrc

ENV ENV="/root/.ashrc" \
    PIP_FORCE_REINSTALL="true" \
    PIP_NO_CACHE_DIR="no" \
    PIP_NO_COMPILE="no"

RUN apk update && \
    apk add --no-cache ca-certificates tini && \
    pip install \
        pykafka==2.7.0 \
        Templer==1.1.4 && \
    rm -rf /var/cache/apk/* && \
    rm -rf /tmp/* && \
    rm -rf /var/log/*

# Get values from child images
ONBUILD ARG REPO_PATH
ONBUILD ARG BRANCH
ONBUILD ARG CONSTRAINTS_BRANCH
ONBUILD ARG CONSTRAINTS_PATH=http://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt
ONBUILD ARG EXTRA_DEPS

# Only needed if you want to persist the value that was used in the image's `env`
# ONBUILD ENV REPO_PATH=$REPO_PATH

ONBUILD WORKDIR /app

ONBUILD RUN apk add --no-cache --virtual .build-deps \
                git make g++ linux-headers && \
            git clone $REPO_PATH . && \
            git reset --hard $BRANCH && \
            pip3 install $EXTRA_DEPS \
                -c $CONSTRAINTS_PATH?h=$CONSTRAINTS_BRANCH && \
            pip3 install /app/. \
                -r /app/requirements.txt \
                -c $CONSTRAINTS_PATH?h=$CONSTRAINTS_BRANCH && \
            apk del .build-deps && \
            rm -rf /var/cache/apk/* && \
            rm -rf /tmp/* && \
            rm -rf /var/log/*

ENTRYPOINT ["/sbin/tini", "-s", "--"]
