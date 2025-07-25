from backend.core.celery_app import celery_app 
from time import sleep
from sqlmodel import Session
from backend.models.job import Job
from backend.core.db import engine
import os



@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def generate_image_task(self, job_id: str, prompt: str, params: dict):
    try:
        result_path = f"results/{job_id}.txt"
        os.makedirs("results", exist_ok=True)
        with open(result_path, "w") as f:
            f.write(f"Generated image for prompt: {prompt}")

        with Session(engine) as session:
            job = session.get(Job, job_id)
            job.status = "completed"
            job.result_path = result_path
            session.add(job)
            session.commit()
    except Exception as e:
        with Session(engine) as session:
            job = session.get(Job, job_id)
            job.status = "failed"
            job.error_message = str(e)
            session.add(job)
            session.commit()
        raise e