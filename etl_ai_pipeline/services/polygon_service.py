from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import asyncio
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential
from ..services.models import StockDatas, PolygonAPIError

import aiohttp
from ..settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PolygonService:
    """Service for interacting with the Polygon.io API."""
    def __init__(self):
        """Initialize the Polygon API service."""
        self.api_key = settings.POLYGON_API_KEY
        if not self.api_key:
            raise ValueError("Missing Polygon API key in environment variables")
        
        self.base_url = "https://api.polygon.io/v1"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def get_stock_data(self, ticker: str, date: str) -> StockDatas:
        """
        Fetch stock data for a specific ticker and date.
        
        Args:
            ticker: Stock ticker symbol
            date: Date in YYYY-MM-DD format
            
        Returns:
            StockDatas object containing the fetched data
            
        Raises:
            PolygonAPIError: If API request fails
        """
        url = f"{self.base_url}/open-close/{ticker}/{date}"
        params = {
            "adjusted": "true",
            "apiKey": self.api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        error_msg = await response.text()
                        logger.error(f"Polygon API error: {error_msg}")
                        raise PolygonAPIError(f"API request failed with status {response.status}: {error_msg}")
                    
                    data = await response.json()
                    
                    return StockDatas(
                        ticker=data["symbol"],
                        date=data["from"],
                        open_price=data["open"],
                        high_price=data["high"],
                        low_price=data["low"],
                        close_price=data["close"],
                        after_hours_price=data.get("afterHours"),
                        pre_market_price=data.get("preMarket"),
                        volume=data["volume"],
                        status=data["status"]
                    )
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error while fetching stock data: {e}")
            raise PolygonAPIError(f"Network error: {str(e)}")
        except KeyError as e:
            logger.error(f"Invalid response format from Polygon API: {e}")
            raise PolygonAPIError(f"Invalid response format: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while fetching stock data: {e}")
            raise PolygonAPIError(f"Unexpected error: {str(e)}")
        

if __name__ == "__main__":
    polygon_service = PolygonService()
    stock_data = asyncio.run(polygon_service.get_stock_data("TSLA", "2025-02-20"))
    print('Stock data: ', stock_data)

