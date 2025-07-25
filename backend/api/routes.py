# backend/api/routes.py

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import uuid
from backend.tasks.worker import generate_image_task
from backend.models.job import Job
from backend.core.db import async_session
import json

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str
    parameters : dict

@router.post("/generate")
async def generate(request: GenerateRequest):
    job_id = str(uuid.uuid4())
    print(f"[API] Generating job_id={job_id}")
    async with async_session() as session:
        job = Job(id=job_id, prompt=request.prompt, parameters=json.dumps(request.parameters))
        session.add(job)
        await session.commit()
    print("[API] Submitting task to Celery")
    generate_image_task.delay(job_id, request.prompt, request.parameters)
    print("[API] Task submitted")
    return {"job_id": job_id}

@router.get("/status/{job_id}")
async def get_status(job_id: str):
    async with async_session() as session:
        job = await session.get(Job, job_id)
        if not job:
            return {"error": "Job not found"}
        return {
            "job_id": job.id,
            "status": job.status,
            "result": job.result_path,
            "error": job.error_message
        }

