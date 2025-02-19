from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(..., example="0.1.0")

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None