from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import uuid
from backend.tasks.worker import generate_image_task


