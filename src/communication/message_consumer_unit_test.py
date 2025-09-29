# python
import unittest
from unittest.mock import patch, MagicMock
from src.communication.message_consumer import MessageConsumer

def handle_message(message: str):
    print(f"Handled message: {message}")

class TestMessageConsumer(unittest.TestCase):
    def setUp(self):
        self.topic = 'test'
        self.env = 'staging'
        self.consumer = MessageConsumer(self.topic, self.env)

    def test_on_message(self):
        @self.consumer.on_message
        def process_message(message: str):
            print(f"Processed message: {message}")

        process_message()

    def test_get_messages(self):
        messages = self.consumer.get_messages(1, 5.0)
        print(messages)
        self.assertIsInstance(messages, list)

    def test_process_messages(self):
        self.consumer.process_messages(handle_message)

if __name__ == '__main__':
    unittest.main()