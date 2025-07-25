# backend/services/replicate_service.py

import httpx
import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    replicate_api_token: str
    replicate_model_version: str

    class Config:
        env_file = ".env"

settings = Settings()

async def generate_image(prompt: str) -> Optional[str]:
    headers = {
        "Authorization": f"Token {settings.replicate_api_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "version": settings.replicate_model_version,
        "input": {
            "prompt": prompt
        }
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "https://api.replicate.com/v1/predictions",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        prediction = response.json()

        status = prediction.get("status")
        get_url = prediction["urls"]["get"]

        
        while status not in ["succeeded", "failed"]:
            await httpx.AsyncClient().get(get_url)
            response = await client.get(get_url, headers=headers)
            status = response.json().get("status")

        if status == "succeeded":
            return response.json().get("output")[0]
        else:
            raise Exception("Replicate job failed")
