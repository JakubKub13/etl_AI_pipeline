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
        Vypočíta volatilitu za posledné 3 dni pre daný ticker.
        
        Metriky:
        1. Denná volatilita = ((High - Low) / Open) * 100
        2. Priemerná 3-dňová volatilita
        3. Cenový rozsah (High - Low)
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
        Identifikuje krátkodobé trendy na základe 3-dňových dát.
        
        Analýza:
        1. Intraday trend (na základe Open vs Close)
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