#!/usr/bin/env python
# coding=utf-8

# (C) Copyright 2017 Hewlett Packard Enterprise Development LP
# (C) Copyright 2018 FUJITSU LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Wait for specific Kafka topics."""

from __future__ import print_function

import logging
import os
import time

from pykafka import KafkaClient

LOG_LEVEL = logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO'))
logging.basicConfig(level=LOG_LEVEL)

logger = logging.getLogger(__name__)

KAFKA_HOSTS = os.environ.get('KAFKA_URI', 'kafka:9092')

KAFKA_WAIT_RETRIES = int(os.environ.get('KAFKA_WAIT_RETRIES', '24'))
KAFKA_WAIT_INTERVAL = int(os.environ.get('KAFKA_WAIT_INTERVAL', '5'))

REQUIRED_TOPICS = os.environ.get('KAFKA_WAIT_FOR_TOPICS', '').split(',')


class TopicNoPartition(Exception):
    """Raise when topic has no partitions."""


class TopicNotFound(Exception):
    """Raise when topic was not found."""


def retry(retries=5, delay=2.0, exc_types=(TopicNoPartition, TopicNotFound)):
    """Retry decorator."""
    def decorator(func):
        def f_retry(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except exc_types as exc:
                    if i < retries - 1:
                        logger.info('Connection attempt %d of %d failed',
                                    i, retries)
                        logger.debug('Caught exception, retrying...',
                                     exc_info=True)
                    else:
                        logger.exception('Failed after %d attempts', retries)
                        logger.exception('Exception was: %r', exc)

                        raise

                # No exception so wait before retrying
                time.sleep(delay)

        return f_retry
    return decorator


@retry(retries=KAFKA_WAIT_RETRIES, delay=KAFKA_WAIT_INTERVAL)
def check_topics(client, req_topics):
    """Check for existence of provided topics in Kafka."""
    for req_topic in req_topics:
        if req_topic in client.topics:
            topic = client.topics[req_topic]
            if topic.partitions:
                logger.info('Topic is ready: %s', req_topic)
            else:
                raise TopicNoPartition('Topic has no partitions: {}'.
                                       format(req_topic))
        else:
            raise TopicNotFound('Topic not found: {}'.format(req_topic))


def main():
    """Main starting point."""

    logger.info('Checking for available topics: %r', repr(REQUIRED_TOPICS))

    client = KafkaClient(hosts=KAFKA_HOSTS)
    check_topics(client, REQUIRED_TOPICS)


if __name__ == '__main__':
    main()
