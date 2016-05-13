# Copyright (c) 2016 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
import unittest

from monasca_common.kafka.producer import KafkaProducer


class KafkaTests(unittest.TestCase):

    def setUp(self):
        self.mock_kafka_client = mock.patch('kafka.client').start()
        self.mock_kafka_producer = mock.patch('kafka.producer').start()
        self.producer = self.mock_kafka_producer.KeyedProducer.return_value
        self.client = self.mock_kafka_client.KafkaClient.return_value

    def tearDown(self):
        self.mock_kafka_client.stop()
        self.mock_kafka_producer.stop()

    def test_kafka_producer_init(self):
        url = 'fake_url'

        KafkaProducer(url)

        self.mock_kafka_client.KafkaClient.assert_called_once_with(url)
        self.mock_kafka_producer.KeyedProducer.assert_called_once_with(
            self.client, async=False,
            req_acks=self.mock_kafka_producer.KeyedProducer
                .ACK_AFTER_LOCAL_WRITE,
            ack_timeout=2000)

    def test_kafka_producer_publish(self):
        producer = KafkaProducer('')
        topic = 'topic'
        messages = ['message']
        key = 'key'

        producer.publish(topic, messages, key)

        self.producer.send_messages.assert_called_once_with(topic, key,
                                                            *messages)

    @mock.patch('monasca_common.kafka.producer.time')
    def test_kafka_producer_publish_one_message_without_key(self, mock_time):
        producer = KafkaProducer('')
        topic = 'topic'
        message = 'not_a_list'
        mock_time.time.return_value = 1
        expected_key = '1000'

        producer.publish(topic, message)

        self.assertTrue(mock_time.time.called)
        self.producer.send_messages.assert_called_once_with(
            topic, expected_key, message)

    @mock.patch('monasca_common.kafka.producer.log')
    def test_kafka_producer_publish_exception(self, mock_logger):
        class MockException(Exception):
            pass

        producer = KafkaProducer('')
        topic = 'topic'
        messages = ['message']
        key = 'key'
        self.producer.send_messages.side_effect = MockException

        try:
            producer.publish(topic, messages, key)
        except MockException:
            pass

        mock_logger.exception.assert_called_once_with(
            'Error publishing to {} topic.'. format(topic))
