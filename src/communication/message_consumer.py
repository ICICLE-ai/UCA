from functools import wraps
from typing import Any, Dict
import json
from confluent_kafka import Consumer
from .config import KafkaConfig

# message -> json
def _convert_message(message: Any):
    return json.loads(message.decode('utf-8').replace("'", '"'))


class MessageConsumer:
    def __init__(self, topic: str, env: str = 'local', override_conf: Dict[str, Any] = None):
        conf = override_conf or KafkaConfig.get_conf(env)
        self.consumer = Consumer(conf)
        self.topic = topic

    def _polling(self):
        self.consumer.subscribe([self.topic])
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue
                yield _convert_message(msg.value())
        except KeyboardInterrupt:
            print("Consumer stopped.")
        finally:
            self.consumer.close()

    def process_messages(self, callback, *args, **kwargs):
        self.consumer.subscribe([self.topic])
        try:
            for message in self._polling():
                callback(message, *args, **kwargs)
        except Exception as e:
            print(f"Error processing messages: {e}")


    def on_message(self, func):
        """Decorator to process messages."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.consumer.subscribe([self.topic])
            for message in self._polling():
                func(message, *args, **kwargs)
        return wrapper

    def get_messages(self, message_count: int = 1, timeout: float = 1.0)-> list[Dict[str, Any]]:
        """
        Fetch a specific number of messages.
        :param message_count: Number of messages to fetch.
        :param timeout: Kafka connection timeout in seconds. If no message is received within this time, stop polling.
        """
        messages = []
        self.consumer.subscribe([self.topic])
        try:
            while len(messages) < message_count:
                msg = self.consumer.poll(timeout)
                if msg is None:
                    break
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue
                messages.append(_convert_message(msg.value()))
        except Exception as e:
            print(f"Error fetching messages: {e}")
        finally:
            self.consumer.close()
        return messages