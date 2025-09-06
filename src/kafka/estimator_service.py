from kafka_client import get_consumer, get_producer
from model_commons.patra.model_card_wrapper import ModelCardWrapper
import torch

model_registry = {
    "nfl": "UCA/src/model_commons/patra/nfl_game_score.pth"
}

model_card = ModelCardWrapper()
consumer = get_consumer("predict.req.time", "time-estimator")
producer = get_producer()

for msg in consumer:
    job = msg.value
    model_name = job.get("model")
    model_path = model_registry.get(model_name.lower())

    if model_path is None:
        print(f"[TimeEstimator] Unknown model: {model_name}")
        continue

    model_instance = model_card.load_model(model_name.lower(), model_path)
    input_tensor = model_instance.prepare_input(job)
    pred = model_instance.predict(input_tensor)

    producer.send("predict.res.time", {
        "job_id": job["job_id"],
        "predicted_time": float(pred)
    })
    producer.flush()