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
