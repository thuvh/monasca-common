FROM python:2.7.14-alpine3.7

COPY wait-for.sh kafka_wait_for_topics.py /

RUN apk update && \
    apk add --no-cache ca-certificates tini && \
    pip install pykafka

ENTRYPOINT ["/sbin/tini", "-s", "--"]
