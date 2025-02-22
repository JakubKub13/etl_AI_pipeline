import asyncio
import logging
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from uuid import UUID

from ..settings import settings
from ..services.models import StockDatas
from .models import StockData, StockAnalysis, StockStatus, MarketSentiment, DatabaseError
from supabase.client import Client, create_client
from supabase.lib.client_options import ClientOptions
from postgrest import APIResponse
from tenacity import retry, stop_after_attempt, wait_exponential

from ..services.polygon_service import PolygonService

logger = logging.getLogger(__name__)

class StockDataManager:
    """Manager for stock data operations in Supabase."""

    def __init__(self, max_connections: int = settings.MAX_CONNECTIONS):
        """Initialize the stock data manager with connection pooling."""
        self._init_supabase_client(max_connections)

    def _init_supabase_client(self, max_connections: int) -> None:
        """Initialize Supabase client with connection pooling."""
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
            raise ValueError("Missing Supabase credentials in environment variables")
        
        self.pool = ThreadPoolExecutor(max_workers=max_connections)
        self.client_options = ClientOptions(
            schema="public",
            headers={"X-Client-Info": "etl-ai-pipeline/production"},
            postgrest_client_timeout=30
        )
        
        try:
            self.client: Client = create_client(
                settings.SUPABASE_URL, 
                settings.SUPABASE_SERVICE_KEY,
                options=self.client_options
            )
            logger.info("Successfully initialized Supabase client")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise DatabaseError(f"Database initialization failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def save_stock_data_with_analysis(
        self, 
        stock_data: StockDatas, 
        analysis_data: Dict[str, Any]
    ) -> Tuple[StockData, StockAnalysis]:
        """
        Save both stock data and its analysis to Supabase.
        
        Args:
            stock_data: Raw stock market data
            analysis_data: AI-enhanced analysis data
            
        Returns:
            Tuple of saved StockData and StockAnalysis objects
            
        Raises:
            DatabaseError: If data insertion fails
        """
        try:
            # Prepare stock data
            stock_data_dict = {
                "ticker": stock_data.ticker,
                "date": stock_data.date,
                "open_price": stock_data.open_price,
                "high_price": stock_data.high_price,
                "low_price": stock_data.low_price,
                "close_price": stock_data.close_price,
                "after_hours_price": stock_data.after_hours_price,
                "pre_market_price": stock_data.pre_market_price,
                "volume": stock_data.volume,
                "status": stock_data.status
            }

            # Save stock data
            stock_result = await asyncio.get_event_loop().run_in_executor(
                self.pool,
                lambda: self.client.table("stock_data")
                    .insert(stock_data_dict)
                    .execute()
            )
            
            if not stock_result.data:
                raise DatabaseError("No data returned from stock data insertion")
            
            saved_stock = stock_result.data[0]
            
            # Prepare analysis data
            analysis_dict = {
                "stock_data_id": saved_stock["id"],
                "llm_analysis": analysis_data["llm_analysis"],
                "market_sentiment": analysis_data["market_sentiment"],
                "model_version": "claude-3-5-sonnet-20240620"
            }

            # Save analysis data
            analysis_result = await asyncio.get_event_loop().run_in_executor(
                self.pool,
                lambda: self.client.table("stock_analysis")
                    .insert(analysis_dict)
                    .execute()
            )
            
            if not analysis_result.data:
                raise DatabaseError("No data returned from analysis insertion")
            
            saved_analysis = analysis_result.data[0]
            
            # Convert to domain models
            stock_data_model = StockData(
                id=UUID(saved_stock["id"]),
                ticker=saved_stock["ticker"],
                date=datetime.fromisoformat(saved_stock["date"]),
                open_price=saved_stock["open_price"],
                high_price=saved_stock["high_price"],
                low_price=saved_stock["low_price"],
                close_price=saved_stock["close_price"],
                after_hours_price=saved_stock.get("after_hours_price"),
                pre_market_price=saved_stock.get("pre_market_price"),
                volume=saved_stock["volume"],
                status=StockStatus(saved_stock["status"]),
                created_at=datetime.fromisoformat(saved_stock["created_at"]),
                updated_at=datetime.fromisoformat(saved_stock["updated_at"])
            )
            
            analysis_model = StockAnalysis(
                id=UUID(saved_analysis["id"]),
                stock_data_id=UUID(saved_analysis["stock_data_id"]),
                llm_analysis=saved_analysis["llm_analysis"],
                market_sentiment=MarketSentiment(saved_analysis["market_sentiment"]),
                model_version=saved_analysis["model_version"],
                created_at=datetime.fromisoformat(saved_analysis["created_at"]),
                updated_at=datetime.fromisoformat(saved_analysis["updated_at"])
            )
            
            logger.info(f"Successfully saved stock data and analysis for {stock_data_model.ticker}")
            return stock_data_model, analysis_model
            
        except Exception as e:
            logger.error(f"Failed to save stock data with analysis: {e}")
            raise DatabaseError(f"Data insertion failed: {str(e)}")

    async def get_stock_data(self, ticker: str, date: str) -> Optional[StockData]:
        """Retrieve stock data by ticker and date."""
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                self.pool,
                lambda: self.client.table("stock_data")
                    .select("*")
                    .eq("ticker", ticker)
                    .eq("date", date)
                    .limit(1)
                    .execute()
            )
            
            if not result.data:
                return None
                
            data = result.data[0]
            return StockData(
                id=UUID(data["id"]),
                ticker=data["ticker"],
                date=datetime.fromisoformat(data["date"]),
                open_price=data["open_price"],
                high_price=data["high_price"],
                low_price=data["low_price"],
                close_price=data["close_price"],
                after_hours_price=data.get("after_hours_price"),
                pre_market_price=data.get("pre_market_price"),
                volume=data["volume"],
                status=StockStatus(data["status"]),
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            )
        except Exception as e:
            logger.error(f"Failed to retrieve stock data: {e}")
            raise DatabaseError(f"Data retrieval failed: {str(e)}")

if __name__ == "__main__":
    stock_data_manager = StockDataManager()
    print("Stock data manager initialized")

    polygon_service = PolygonService()
    stock_data = asyncio.run(polygon_service.get_stock_data("MSFT", "2025-02-20"))
    print('Received stock data from Polygon:', stock_data)

    analysis_data = {
        "llm_analysis": "This is a sample analysis",
        "market_sentiment": "Positive",
        "price_movement_summary": "Stock price increased",
        "trading_volume_analysis": "High trading volume"
    }

    saved_stock_data, saved_analysis = asyncio.run(stock_data_manager.save_stock_data_with_analysis(stock_data, analysis_data))
    print('Saved stock data: ', saved_stock_data)
    print('Saved analysis: ', saved_analysis)



    
