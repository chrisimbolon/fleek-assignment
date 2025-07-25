from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Job(SQLModel, table = True):
    id: str = Field(primary_key=True)
    prompt: str
    parameters: str
    status: str = "pending"
    result_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)