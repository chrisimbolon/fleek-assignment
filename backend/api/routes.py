from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import uuid
from backend.tasks.worker import generate_image_task

router = APIRouter

class GenerateRequest(BaseModel):
    prompt: str
    parameters : dict

@router.post("/generate")
async def generate(request : GenerateRequest):
    job_id = str(uuid.uuid4())
    generate_image_task.delay(job_id, request.prompt, request.parameters)
    return {"job_id": job_id}

@router.get("/status/{job_id}")
async def get_status(job_id:str):
    # TODO: Rejplace with real DB call 
    return {"job_id": job_id, "status": "pending", "result": None}
