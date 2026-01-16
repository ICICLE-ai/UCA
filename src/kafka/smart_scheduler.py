import threading
from kafka_client import get_producer, get_consumer

class SmartScheduler:
    def __init__(self):
        self.producer = get_producer()

    def send_time_estimation_request(self, job):
        self.producer.send("predict.req.time", job)
        self.producer.flush()

    def send_ckn_request(self, job):
        self.producer.send("predict.req.ckn", job)
        self.producer.flush()

    def listen_for_time_response(self):
        consumer = get_consumer("predict.res.time", "smart-scheduler")
        for msg in consumer:
            print(f"[SmartScheduler] Received time estimate: {msg.value}")

    def listen_for_ckn_response(self):
        consumer = get_consumer("predict.res.ckn", "smart-scheduler")
        for msg in consumer:
            print(f"[SmartScheduler] Received CKN output: {msg.value}")

    def start(self):
        threading.Thread(target=self.listen_for_time_response, daemon=True).start()
        threading.Thread(target=self.listen_for_ckn_response, daemon=True).start()
