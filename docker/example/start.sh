#!/bin/sh

# Test services we need before starting our service.
python3 /kafka_wait_for_topics.py || exit 1

# Template all config files before start, it will use env variables.
# Read usage examples: https://pypi.org/project/Templer/
templer /*.j2 /

# Start our service.
# gunicorn --args
echo "Hello from start.sh"
