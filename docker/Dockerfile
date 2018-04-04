FROM python:3.5.5-alpine3.4

COPY wait-for.sh kafka_wait_for_topics.py /
COPY ashrc /root/.ashrc

ENV ENV="/root/.ashrc" \
    PIP_FORCE_REINSTALL="true" \
    PIP_NO_CACHE_DIR="no" \
    PIP_NO_COMPILE="no"

RUN apk update && \
    apk add --no-cache ca-certificates tini && \
    pip install pykafka

ENTRYPOINT ["/sbin/tini", "-s", "--"]
