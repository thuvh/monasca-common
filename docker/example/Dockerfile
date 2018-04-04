ARG REPO_PATH=https://git.openstack.org/cgit/openstack/monasca-api
# Branch, tag or git hash to build from.
ARG BRANCH=master
ARG CONSTRAINTS_BRANCH=master
ARG EXTRA_DEPS="gunicorn influxdb python-memcached Jinja2"

FROM monasca-base:latest

ENV KAFKA_URI=kafka:9092 \
    KAFKA_WAIT_FOR_TOPICS=alarm-state-transitions,metrics

COPY start.sh config_1.yml.j2 config_2.yml.j2 /

CMD ["/start.sh"]
