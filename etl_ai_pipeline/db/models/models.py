from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
from uuid import UUID


class StockStatus(str, Enum):
    OK = "OK"
    NOT_FOUND = "NOT_FOUND"
    ERROR = "ERROR"

class MarketSentiment(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"

@dataclass
class StockData:
    """Stock data model representing raw market data."""
    id: UUID
    ticker: str
    date: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    after_hours_price: Optional[float]
    pre_market_price: Optional[float]
    volume: float
    status: StockStatus
    created_at: datetime
    updated_at: datetime

@dataclass
class StockAnalysis:
    """Stock analysis model representing AI-enhanced data."""
    id: UUID
    stock_data_id: UUID
    llm_analysis: str
    market_sentiment: MarketSentiment
    model_version: str
    created_at: datetime
    updated_at: datetime
class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass