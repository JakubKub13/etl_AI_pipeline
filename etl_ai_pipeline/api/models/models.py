from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


from ...settings import settings
class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(..., example=settings.APP_VERSION)

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

class StockDataRequest(BaseModel):
    ticker: str
    date: str

class AnalysisEmailConfig(BaseModel):
    recipient_email: EmailStr
    subject: Optional[str] = None
    cc: Optional[List[EmailStr]] = None

class StockAnalysisRequest(BaseModel):
    ticker: str
    email_config: AnalysisEmailConfig