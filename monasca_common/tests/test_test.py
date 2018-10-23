import mock
from monasca_common.confluent_kafka import producer
from oslotest import base
FAKE_KAFKA_URL = 'FAKE_KAFKA_URL'


class TestConfluentKafkaProducer(base.BaseTestCase):

    def setUp(self):
        super(TestConfluentKafkaProducer, self).setUp()
        self.confluent_kafka_patcher = \
            mock.patch('monasca_common.confluent_kafka.producer.confluent_kafka')
        self.mock_confluent_kafka = self.confluent_kafka_patcher.start()
        self.producer = self.mock_confluent_kafka.Producer.return_value
        self.monasca_kafka_producer = producer.KafkaProducer(FAKE_KAFKA_URL)

    def tearDown(self):
        super(TestConfluentKafkaProducer, self).tearDown()
        self.confluent_kafka_patcher.stop()

    def test_kafka_producer_init(self):
        self.assertTrue(self.mock_confluent_kafka.Producer.called)
