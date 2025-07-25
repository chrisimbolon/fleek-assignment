#backend/tasks/worker.py

from backend.core.celery_app import celery_app 
from time import sleep
from sqlmodel import Session
from backend.models.job import Job
from backend.core.db import sync_session
import os
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def generate_image_task(self, job_id: str, prompt: str, parameters: dict):
    print(f"[TASK STARTED] job_id={job_id}")

    with sync_session() as session:
        job = session.get(Job, job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")

        # simulating image generation
        path = f"results/{job_id}.txt"
        with open(path, "w") as f:
            f.write(f"Generated: {prompt} with {parameters}")

        job.status = "completed"
        job.result_path = path
        session.add(job)
        session.commit()

    print(f"[TASK COMPLETED] job_id={job_id}")
    return {"status": "done", "path": path}
