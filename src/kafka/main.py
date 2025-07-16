from smart_scheduler.smart_scheduler import SmartScheduler
import time

if __name__ == "__main__":
    scheduler = SmartScheduler()
    scheduler.start()

    test_job = {
        "job_id": "job_001",
        "model": "nfl",
        "resource": 32,
        "input_size": 2048,
        "env_status": {"load": 0.7},
        "job_info": {"priority": "high"}
    }

    scheduler.send_time_estimation_request(test_job)
    scheduler.send_ckn_request(test_job)

    while True:
        time.sleep(1)
