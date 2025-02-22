from typing import TypedDict, Optional
from ...services.models import StockDatas

class StockDataState(TypedDict):
    """State for stock data processing workflow."""
    ticker: str
    date: str
    raw_data: Optional[StockDatas]
    enhanced_data: Optional[dict]
    final_data: Optional[dict]
