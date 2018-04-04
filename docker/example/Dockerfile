# Example Dockerfile for creating Docker image.

ARG REPO_PATH=https://git.openstack.org/openstack/monasca-api
# Branch, tag or git hash to build from.
ARG VERSION=master
ARG CONSTRAINTS_BRANCH=master
# Extra Python3 dependencies.
ARG EXTRA_DEPS="gunicorn influxdb python-memcached Jinja2"

# Always start from `monasca-base` image and use specific version of it.
FROM monasca-base:1.0.0

# Environment variables used for our service or wait scripts.
ENV \
    KAFKA_URI=kafka:9092 \
    KAFKA_WAIT_FOR_TOPICS=alarm-state-transitions,metrics \
    MYSQL_HOST=mysql \
    MYSQL_USER=monapi \
    MYSQL_PASSWORD=password \
    MYSQL_DB=mon \
    LOG_LEVEL=INFO

# Copy all neccessary files to proper locations.
COPY config_1.yml.j2 config_2.yml.j2 /

# Run here all additionals steps your service need post installation.
# Stay with only one `RUN` and use `&& \` for next steps to don't create
# unnecessary image layers. Clean at the end to conserve space.
RUN \
    echo "Some steps to do after main installation." && \
    echo "Hello when building."

# Use healthcheck functionality to provide information for Docker if service
# running inside container is healthy. Avoid using `curl` directly and instead
# use `healthcheck.py` written with specific service in mind. It will provide
# more flexibility like when creating JSON request body.
HEALTHCHECK CMD python3 healthcheck.py || exit 1

CMD ["/start.sh"]
