from backend.core.celery_app import celery
from time import sleep

@celery.task(bind=True, autoretry_for(Exception,) retry_backoff=True)
def generate_image_task(self, job_id:str, prompt: str, params: dict)
    #mocking Replicate Call
    print(f"[{job_id}] Generating image for : {prompt} with params: {params}")
    sleep(5)
    print(f"[{job_id}] Done.")
    # TODO: Save result to DB and file system