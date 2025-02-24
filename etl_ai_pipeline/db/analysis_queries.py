from typing import Dict, List
import logging
from datetime import datetime, timedelta
from ..db.Stock_data_manager import StockDataManager

logger = logging.getLogger(__name__)

class StockAnalyzer:
    def __init__(self, stock_data_manager: StockDataManager):
        self.manager = stock_data_manager

    async def calculate_short_term_volatility(self, ticker: str) -> Dict:
        """
        Calculates volatility for the last 3 days for a given ticker.
        
        Metrics:
        1. Daily volatility = ((High - Low) / Open) * 100
        2. Average 3-day volatility
        3. Price range (High - Low)
        """
        return await self.manager.execute_query(
            'execute_stock_analysis',
            {
                "p_ticker": ticker,
                "p_days": 3
            }
        )

    async def identify_short_term_trends(self, ticker: str) -> Dict:
        """
        Identifies short-term trends based on 3-day data.
        
        Analysis:
        1. Intraday trend (based on Open vs Close)
        2. Price momentum
        3. Volume trend
        """
        return await self.manager.execute_query(
            'execute_trend_analysis',
            {
                "p_ticker": ticker,
                "p_days": 3
            }
        )