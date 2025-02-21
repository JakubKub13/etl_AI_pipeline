from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class StockData:
    """Stock data model representing the database structure."""
    id: str
    ticker: str
    date: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    after_hours_price: Optional[float]
    pre_market_price: Optional[float]
    volume: float
    status: str
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass