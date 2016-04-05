# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
# Copyright 2016 FUJITSU LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import kafka.client
import kafka.partitioner
import kafka.producer
import logging
import time

log = logging.getLogger(__name__)


class KafkaProducer(object):
    """Adds messages to a kafka topic
    """

    def __init__(self, url, round_robin=False):
        """Creates new kafka producer

        Note:
            By default producer is created with
            :py:class:'kafka.partitioner.Murmur2Partitioner'.
            If round robin partitioner (i.e. fair) should be used
            set 'round_robin'=True

        :arg str|tuple|list url: host(s) to connect to
        :arg bool round_robin: should fair round robin partitioner be used

        """

        if round_robin:
            partitioner = kafka.partitioner.RoundRobinPartitioner
        else:
            partitioner = kafka.partitioner.Murmur2Partitioner

        self._kafka = kafka.client.KafkaClient(url)
        self._producer = kafka.producer.KeyedProducer(
            self._kafka,
            async=False,
            req_acks=kafka.producer.KeyedProducer.ACK_AFTER_LOCAL_WRITE,
            ack_timeout=2000,
            partitioner=partitioner)

    def publish(self, topic, messages, key=None):
        """Takes messages and puts them on the supplied kafka topic

        :param str topic: target topic
        :param list|str messages: single message or list of messages
        :param str key: key for set of messages
        """

        if not isinstance(messages, list):
            messages = [messages]

        try:
            if key is None:
                key = int(time.time() * 1000)
            self._producer.send_messages(topic, str(key), *messages)
        except Exception:
            log.exception('Error publishing to {} topic.'.format(topic))
            raise
