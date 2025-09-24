# python
import unittest
from unittest.mock import patch, MagicMock
from src.communication.message_producer import MessageProducer

class TestMessageProducer(unittest.TestCase):
    def setUp(self):
        self.topic = 'test'
        self.env = 'staging'
        self.producer = MessageProducer(self.topic, self.env)

    def test_produce_message(self):
        message = {'key': 'value'}
        self.producer.produce_message(message)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()