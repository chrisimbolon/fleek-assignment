# backend/core/celery_app.py

import os
from celery import Celery

REDIS_HOST = os.getenv("REDIS_HOST", "localhost") 

celery_app = Celery(
    __name__,
    broker=f'redis://{REDIS_HOST}:6379/0',
    backend=f'redis://{REDIS_HOST}:6379/0'
)

celery_app.conf.task_routes = {
    "backend.tasks.worker.*": {"queue": "default"}
}

from backend.tasks import worker