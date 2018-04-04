FROM python:3.5.5-alpine3.4

COPY wait-for.sh kafka_wait_for_topics.py /

RUN apk update && \
    apk add --no-cache ca-certificates tini && \
    pip install pykafka

ENTRYPOINT ["/sbin/tini", "-s", "--"]
