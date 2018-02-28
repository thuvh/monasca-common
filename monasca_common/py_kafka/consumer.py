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

from pykafka import KafkaClient


class KafkaConsumer(object):
    def __init__(self, kafka_url, topic, consumer_group, zookeeper_url):
        client = KafkaClient(hosts=kafka_url)
        self.consumer = client.topics[topic].\
            get_balanced_consumer(consumer_group=consumer_group,
                                  auto_commit_enable=True, zookeeper_connect=zookeeper_url)

    def __iter__(self):
        for message in self.consumer:
            if message is not None:
                yield message
