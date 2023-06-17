from confluent_kafka import Producer
from configs.earthquakeKafka import get_conf

default_conf = get_conf()
conf = {
    "bootstrap.servers": default_conf.get("bootstrap.servers"),
    "client.id": "earthquake-producer",
}


class KafkaProducer:
    def __init__(self, topic):
        self.producer = Producer(conf)
        self.topic = topic

    def __ack_callback(self, err, msg):
        if err is not None:
            print("Failed to deliver message: {0}: {1}".format(msg.value(), err.str()))
        else:
            message = str(msg.value(), "utf-8")
            print("Message produced: {0}".format(message))

    def produce(self, message: str):
        self.producer.produce(self.topic, message, callback=self.__ack_callback)
        self.producer.poll(0)
        self.flush()

    def flush(self):
        self.producer.flush()
