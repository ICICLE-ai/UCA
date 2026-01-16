import json
from kafka import KafkaProducer, KafkaConsumer

BOOTSTRAP_SERVERS = ['localhost:9092']

def get_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def get_consumer(topic, group_id):
    return KafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=group_id,
        auto_offset_reset='earliest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

