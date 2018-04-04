FROM python:3.5.5-alpine3.7

COPY wait_for.sh kafka_wait_for_topics.py /
COPY ashrc /root/.ashrc

ENV \
    ENV="/root/.ashrc" \
    PIP_FORCE_REINSTALL="true" \
    PIP_NO_CACHE_DIR="no" \
    PIP_NO_COMPILE="no"

RUN \
    chmod +x /wait_for.sh /kafka_wait_for_topics.py && \
    apk update && \
    apk add --no-cache \
        ca-certificates su-exec tini tzdata && \
    pip install \
        pykafka==2.7.0 \
        Templer==1.1.4 && \
    rm -rf /var/cache/apk/* && \
    rm -rf /tmp/* && \
    rm -rf /var/log/*

# Get values from child images
ONBUILD ARG REPO_PATH
ONBUILD ARG VERSION
ONBUILD ARG CONSTRAINTS_BRANCH
ONBUILD ARG CONSTRAINTS_PATH=http://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt
ONBUILD ARG EXTRA_DEPS

# Only needed if you want to persist the value that was used in the image's `env`
# ONBUILD ENV REPO_PATH=$REPO_PATH

ONBUILD WORKDIR /app

ONBUILD RUN \
            apk add --no-cache --virtual .build-deps \
                git make g++ linux-headers && \
            git clone $REPO_PATH . && \
            git reset --hard $VERSION && \
            pip3 install \
                /app/. $EXTRA_DEPS \
                -r /app/requirements.txt \
                -c $CONSTRAINTS_PATH?h=$CONSTRAINTS_BRANCH && \
            printf "Version: %s\n" $VERSION >> /VERSIONS && \
            printf "Revision: %s\n" `git rev-parse HEAD` >> /VERSIONS && \
            apk del .build-deps && \
            rm -rf /var/cache/apk/* && \
            rm -rf /tmp/* && \
            rm -rf /var/log/*

ENTRYPOINT ["/sbin/tini", "-s", "--"]
