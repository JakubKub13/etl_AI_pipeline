from typing import TypedDict, Optional, List, Dict
from ...services.models import StockDatas
from pydantic import BaseModel, EmailStr

class StockDataState(TypedDict):
    """State for stock data processing workflow."""
    ticker: str
    date: str
    raw_data: Optional[StockDatas]
    enhanced_data: Optional[dict]
    final_data: Optional[dict]

class StockAnalysisState(TypedDict):
    """State for stock analysis workflow."""
    ticker: str
    date: str
    trends_data: Optional[List[Dict]]
    volatility_data: Optional[List[Dict]]
    analysis_report: Optional[str]
    email_sent: bool

class EmailConfig(BaseModel):
    """Configuration for email sending."""
    recipient_email: EmailStr
    subject: Optional[str] = None
    cc: Optional[List[EmailStr]] = None