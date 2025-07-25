from fastapi import FastAPI
from backend.api.routes import router
from backend.core.db import init_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(router)