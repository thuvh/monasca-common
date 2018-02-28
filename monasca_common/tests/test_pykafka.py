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

import mock
from mock import patch

from monasca_common.py_kafka import consumer
from monasca_common.py_kafka import producer
from oslotest import base

FAKE_KAFKA_URL = "kafka_url"
FAKE_ZOOKEEPER_URL = "zookeeper_url"
FAKE_ZOOKEEPER_PATH = "zookeeper_path"
FAKE_KAFKA_CONSUMER_GROUP = "group"
FAKE_KAFKA_TOPIC = "topic"


class TestPyKafkaProducer(base.BaseTestCase):

    @patch('pykafka.KafkaClient')
    def setUp(self, mock_kafka_client):
        super(TestPyKafkaProducer, self).setUp()
        self.mock_kafka_client = mock_kafka_client
        self.client = self.mock_kafka_client.return_value
        self.producer = self.client.topics[FAKE_KAFKA_TOPIC].get_sync_producer.return_value
        self.monasca_kafka_producer = producer.KafkaProducer(FAKE_KAFKA_URL, FAKE_KAFKA_TOPIC)
        self.topic = FAKE_KAFKA_TOPIC

    def tearDown(self):
        super(TestPyKafkaProducer, self).tearDown()

    def test_kafka_producer_init(self):
        self.assertTrue(self.mock_kafka_client.called)

    def test_kafka_producer_publish(self):
        messages = ['message']
        key = 'key'

        self.monasca_kafka_producer.publish(messages, key)

        self.producer.produce.assert_called_once_with(messages[0], key)

    @patch('monasca_common.py_kafka.producer.time')
    def test_kafka_producer_publish_one_message_without_key(self, mock_time):

        message = 'not_a_list'
        mock_time.time.return_value = 1
        expected_key = '1000'

        self.monasca_kafka_producer.publish(message)
        self.assertTrue(mock_time.time.called)
        self.producer.produce.assert_called_once_with(message, expected_key)

    @patch('monasca_common.py_kafka.producer.log')
    def test_kafka_producer_publish_exception(self, mock_logger):
        class MockException(Exception):
            pass

        messages = ['message']
        key = 'key'
        self.producer.produce.side_effect = MockException

        self.assertRaises(MockException, self.monasca_kafka_producer.publish,
                          messages, key)

        mock_logger.exception.assert_called_once_with(
            'Error publishing to {} topic.'.format(self.topic))


class TestKafkaConsumer(base.BaseTestCase):
    def setUp(self):
        super(TestKafkaConsumer, self).setUp()
        self.kafka_client_patcher = mock.patch('monasca_common.py_kafka.consumer.KafkaClient')
        self.mock_kafka_client = self.kafka_client_patcher.start()
        self.client = self.mock_kafka_client.return_value
        self.consumer = self.client.topics[FAKE_KAFKA_TOPIC].\
            get_balanced_consumer(consumer_group=FAKE_KAFKA_CONSUMER_GROUP,
                                  auto_commit_enable=True,
                                  zookeeper_connect=FAKE_ZOOKEEPER_URL).return_value
        self.monasca_kafka_consumer = consumer.KafkaConsumer(FAKE_KAFKA_URL,
                                                             FAKE_KAFKA_TOPIC,
                                                             FAKE_KAFKA_CONSUMER_GROUP,
                                                             FAKE_ZOOKEEPER_URL)

    def tearDown(self):
        super(TestKafkaConsumer, self).tearDown()
        self.kafka_client_patcher.stop()

    def test_kafka_consumer_init(self):
        self.assertTrue(self.mock_kafka_client.called)

    def test_kafka_consumer_process_messages(self):
        messages = []
        for i in range(5):
            messages.append("message{}".format(i))
        self.consumer.get_message.side_effect = messages
        for index, message in enumerate(self.monasca_kafka_consumer):
            self.assertEqual(message, messages[index])
