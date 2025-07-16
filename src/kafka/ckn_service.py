from kafka_client import get_consumer, get_producer
from model_commons.patra.model_card_wrapper import ModelCardWrapper
from model_commons.patra.validator import Validator

consumer = get_consumer("predict.req.ckn", "ckn-service")
producer = get_producer()

model_card = ModelCardWrapper()

for msg in consumer:
    job = msg.value
    print(f"[CKN] Received: {job}")

    job_info = job.get("job_info", {})
    env_status = job.get("env_status", {})

    is_valid = True
    try:
        Validator.validate_dict(
            input_dict=job_info,
            keys_mandatory=["priority"],
            keys_mandatory_types=["str"],
            keys_optional=["task_type", "deadline"],
            keys_optional_types=["str", "number"]
        )
    except Exception as e:
        print(f"[CKN] Invalid job_info: {e}")
        is_valid = False

    try:
        category = model_card.classify(job_info)
    except Exception as e:
        print(f"[CKN] ModelCard classification failed: {e}")
        category = "unknown"

    suggestion = "schedule_now" if is_valid and env_status.get("load", 1.0) < 0.8 else "wait"

    resp = {
        "job_id": job["job_id"],
        "category": category,
        "suggestion": suggestion
    }

    producer.send("predict.res.ckn", resp)
    producer.flush()