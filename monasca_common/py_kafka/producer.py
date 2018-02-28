# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import pykafka
import time

log = logging.getLogger(__name__)


class KafkaProducer(object):

    def __init__(self, kafka_url, topic):
        """Init

             kafka_url - Kafka connection details
             topic - Name of Kafka topic
        """

        client = pykafka.KafkaClient(hosts=kafka_url)
        self.topic = topic
        self.producer = client.topics[topic].get_sync_producer()

    def publish(self, messages, key=None):
        """Takes messages and puts them on Kafka

        """

        if not isinstance(messages, list):
            messages = [messages]

        for message in messages:
            try:
                if key is None:
                    key = int(time.time() * 1000)
                self.producer.produce(message, str(key))
            except Exception:
                log.exception('Error publishing to {} topic.'.format(self.topic))
                raise
