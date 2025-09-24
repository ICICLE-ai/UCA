# python
from typing import Any, Dict
from confluent_kafka import Producer
from .config import KafkaConfig

class MessageProducer:
    def __init__(self, topic: str, env: str = 'local', override_conf: Dict[str, Any] = None):
        self.topic = topic
        conf = override_conf or KafkaConfig.get_conf(env)
        self.producer = Producer(conf)

    def produce_message(self, message: Dict[str, Any]):
        self.producer.produce(self.topic, str(message).encode('utf-8'))
        self.producer.flush()