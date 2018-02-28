import pykafka
import logging
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
