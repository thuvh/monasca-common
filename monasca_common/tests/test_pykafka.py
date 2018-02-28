import mock
import monasca_common
from mock import patch

from oslotest import base
from monasca_common.py_kafka import producer
from monasca_common.py_kafka import consumer

class TestPyKafkaProducer(base.BaseTestCase):

    def setUp(self):
        super(TestPyKafkaProducer, self).setUp()

    def tearDown(self):
        super(TestPyKafkaProducer, self).tearDown()

    @patch('pykafka.KafkaClient')
    @patch('monasca_common.py_kafka.producer.time.time', return_value=1)
    def test_kafka_producer_publish(self, mock_client, mock_time):

        # arrange
        prod = producer.KafkaProducer("FAKE-KAFKA-URL", "FAKE-TOPIC")
        prod.publish("test-message")

        # assert
        prod.producer.produce.assert_called_with("test-message", "1000")
