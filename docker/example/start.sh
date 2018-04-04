#!/bin/sh
# Starting script.
# All checks you need to do before service could be safely started should
# be added in this file.

# Test services we need before starting our service.
python3 /kafka_wait_for_topics.py || exit 1
python3 /check_mysql.py || exit 1

# Template all config files before start, it will use env variables.
# Read usage examples: https://pypi.org/project/Templer/
templer /*.j2 /

# Start our service.
# gunicorn --args
echo "Hello from start.sh"

# Allow server to stay alive in case of failure for 2 hours for debugging.
RESULT=$?
if [ $RESULT != 0 ] && [ "$STAY_ALIVE_ON_FAILURE" = "true" ]; then
  sleep 7200
fi
exit $RESULT
