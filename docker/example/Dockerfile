ARG REPO_PATH=https://github.com/openstack/monasca-api
ARG BRANCH=master
ARG CONSTRAINTS_BRANCH=master
ARG EXTRA_DEPS="gunicorn influxdb python-memcached Jinja2"

FROM monasca-base:latest

ENV KAFKA_URI=kafka:9092 \
    KAFKA_WAIT_FOR_TOPICS=alarm-state-transitions,metrics

COPY start.sh /

CMD ["/start.sh"]
