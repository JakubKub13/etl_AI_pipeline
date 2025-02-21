from dataclasses import dataclass
from typing import Optional

@dataclass
class StockDatas:
    """Data model for stock market data."""
    ticker: str
    date: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    after_hours_price: Optional[float]
    pre_market_price: Optional[float]
    volume: float
    status: str


class PolygonAPIError(Exception):
    """Custom exception for Polygon API related errors."""
    pass
