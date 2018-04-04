#!/bin/sh

# Test services we need before starting our service
python3 /kafka_wait_for_topics.py || exit 1

# Template all config files before start

# Start our service
gunicorn --args
