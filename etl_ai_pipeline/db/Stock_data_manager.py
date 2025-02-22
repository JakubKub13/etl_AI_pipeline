import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from ..settings import settings
from ..services.models import StockDatas
from .models import StockData, DatabaseError
from supabase.client import Client, create_client
from supabase.lib.client_options import ClientOptions
from postgrest import APIResponse
from tenacity import retry, stop_after_attempt, wait_exponential

from ..services.polygon_service import PolygonService

logger = logging.getLogger(__name__)

class StockDataManager:
    """Manager for stock data operations in Supabase."""

    def __init__(self, max_connections: int = settings.MAX_CONNECTIONS):
        """
        Initialize the stock data manager with connection pooling.
        
        Args:
            max_connections: Maximum number of concurrent database connections
        """
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_SERVICE_KEY
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Missing Supabase credentials in environment variables")
        
        # Initialize connection pool
        self.pool = ThreadPoolExecutor(max_workers=max_connections)
        
        # Configure client options
        self.client_options = ClientOptions(
            schema="public",
            headers={"X-Client-Info": "supabase-py/production"},
            postgrest_client_timeout=30
        )
        
        # Initialize the client
        try:
            self.client: Client = create_client(
                self.supabase_url, 
                self.supabase_key,
                options=self.client_options
            )
            logger.info("Successfully initialized Supabase client for stock data")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise DatabaseError(f"Database initialization failed: {str(e)}")
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def save_stock_data(self, stock_data: StockDatas) -> StockData:
        """
        Save stock data to Supabase with retry logic.
        
        Args:
            stock_data: Dictionary containing stock data
            
        Returns:
            StockData object
            
        Raises:
            DatabaseError: If data insertion fails
        """
        try:
            print("Incoming stock data:", stock_data)

            data = {
                "ticker": stock_data.ticker,
                "date": stock_data.date,
                "open_price": stock_data.open_price,
                "high_price": stock_data.high_price,
                "low_price": stock_data.low_price,
                "close_price": stock_data.close_price,
                "after_hours_price": stock_data.after_hours_price,
                "pre_market_price": stock_data.pre_market_price,
                "volume": stock_data.volume,
                "status": stock_data.status,
                "created_at": datetime.now(timezone.utc).isoformat()
            }

            print("Prepared data for Supabase:", data) 
                
            result = await asyncio.get_event_loop().run_in_executor(
                self.pool,
                lambda: self.client.table("stock_data").insert(data).execute()
            )
            
            if not result.data:
                raise DatabaseError("No data returned from stock data insertion")
                
            saved_data = result.data[0]
            logger.info(f"Successfully saved stock data for {saved_data['ticker']}")
            
            return StockData(
                id=saved_data["id"],
                ticker=saved_data["ticker"],
                date=datetime.fromisoformat(saved_data["date"]),
                open_price=saved_data["open_price"],
                high_price=saved_data["high_price"],
                low_price=saved_data["low_price"],
                close_price=saved_data["close_price"],
                after_hours_price=saved_data.get("after_hours_price"),
                pre_market_price=saved_data.get("pre_market_price"),
                volume=saved_data["volume"],
                status=saved_data["status"],
                created_at=datetime.fromisoformat(saved_data["created_at"])
            )
            
        except Exception as e:
            logger.error(f"Failed to save stock data: {e}")
            raise DatabaseError(f"Stock data insertion failed: {str(e)}")
        
if __name__ == "__main__":
    stock_data_manager = StockDataManager()
    print("Stock data manager initialized")

    polygon_service = PolygonService()
    stock_data = asyncio.run(polygon_service.get_stock_data("MSFT", "2025-02-20"))
    print('Received stock data from Polygon:', stock_data)


    saved_stock_data = asyncio.run(stock_data_manager.save_stock_data(stock_data))
    print('Saved stock data: ', saved_stock_data)



    
