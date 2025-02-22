## DATA RETRIEVAL WORKFLOW
from typing import TypedDict, Optional
from datetime import datetime
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
import logging
from ...settings import settings
from ...services.polygon_service import PolygonService
from ...db.Stock_data_manager import StockDataManager
from ...services.models import StockDatas
from ...agent.models import StockDataState

logger = logging.getLogger(__name__)

class DataRetrievalGraph:
    """Graph for processing stock data with LLM enhancement."""

    def __init__(self):
        """Initialize the data retrieval workflow."""
        self.polygon_service = PolygonService()
        self.stock_data_manager = StockDataManager()
        self.anthropic = ChatAnthropic(
            model="claude-3-5-sonnet-20240620",
            temperature=0.5,
        )
        self.workflow = self._create_workflow()

    async def fetch_raw_data(self, state: StockDataState) -> dict:
        """Fetch raw stock data from Polygon API."""
        try:
            data = await self.polygon_service.get_stock_data(
                state["ticker"], 
                state["date"]
            )
            print("Raw data fetched:", data)
            return {"raw_data": data}
        except Exception as e:
            logger.error(f"Error fetching raw data: {e}")
            raise

    async def enhance_with_llm(self, state: StockDataState) -> dict:
        """Enhance stock data with LLM analysis."""
        try:
            raw_data = state["raw_data"]
            
            prompt = f"""Analyze this stock data for {raw_data.ticker} on {raw_data.date}:
            - Opening Price: ${raw_data.open_price}
            - Closing Price: ${raw_data.close_price}
            - High: ${raw_data.high_price}
            - Low: ${raw_data.low_price}
            - Volume: {raw_data.volume}
            - After Hours: ${raw_data.after_hours_price if raw_data.after_hours_price else 'N/A'}
            - Pre-market: ${raw_data.pre_market_price if raw_data.pre_market_price else 'N/A'}

            Provide:
            1. Overall market sentiment
            2. Detailed price movement analysis
            3. Trading volume analysis and its significance
            4. Comprehensive summary of the day's trading activity
            """

            response = await self.anthropic.ainvoke(input=prompt)

            analysis = response.content
            print("Analysis:", analysis)
            
            # Parse the analysis into structured data
            enhanced_data = {
                "llm_analysis": analysis,
                "market_sentiment": self._extract_sentiment(analysis),
                "price_movement_summary": self._extract_price_analysis(analysis),
                "trading_volume_analysis": self._extract_volume_analysis(analysis)
            }
            
            return {"enhanced_data": enhanced_data}
        except Exception as e:
            logger.error(f"Error in LLM enhancement: {e}")
            raise

    async def save_to_database(self, state: StockDataState) -> dict:
        """Save enhanced data to database."""
        try:
            raw_data = state["raw_data"]
            enhanced_data = state["enhanced_data"]
            
            # Combine raw and enhanced data
            final_data = StockDatas(
                ticker=raw_data.ticker,
                date=raw_data.date,
                open_price=raw_data.open_price,
                high_price=raw_data.high_price,
                low_price=raw_data.low_price,
                close_price=raw_data.close_price,
                after_hours_price=raw_data.after_hours_price,
                pre_market_price=raw_data.pre_market_price,
                volume=raw_data.volume,
                status=raw_data.status,
                **enhanced_data
            )
            
            saved_data = await self.stock_data_manager.save_stock_data(final_data)
            return {"final_data": saved_data}
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            raise

    def _create_workflow(self) -> StateGraph:
        """Create the workflow graph."""
        workflow = StateGraph(StockDataState)
        
        # Add nodes
        workflow.add_node("fetch_raw_data", self.fetch_raw_data)
        workflow.add_node("enhance_with_llm", self.enhance_with_llm)
        workflow.add_node("save_to_database", self.save_to_database)
        
        # Add edges
        workflow.add_edge(START, "fetch_raw_data")
        workflow.add_edge("fetch_raw_data", "enhance_with_llm")
        workflow.add_edge("enhance_with_llm", "save_to_database")
        workflow.add_edge("save_to_database", END)
        
        return workflow.compile()
    
    @staticmethod
    def _extract_sentiment(analysis: str) -> str:
        """Extract sentiment from LLM analysis."""
        analysis_lower = analysis.lower()
        if "bullish" in analysis_lower:
            return "bullish"
        elif "bearish" in analysis_lower:
            return "bearish"
        return "neutral"

    @staticmethod
    def _extract_price_analysis(analysis: str) -> str:
        """Extract price movement analysis."""
        try:
            # Look for the section starting with "2. Detailed price movement analysis:"
            sections = analysis.split("\n\n")
            for section in sections:
                if "price movement analysis" in section.lower():
                    return section.strip()
            # If not found, return the first paragraph after "2."
            for section in sections:
                if section.strip().startswith("2."):
                    return section.strip()
            return "Price analysis not found"
        except Exception:
            return "Error extracting price analysis"

    @staticmethod
    def _extract_volume_analysis(analysis: str) -> str:
        """Extract volume analysis."""
        try:
            # Look for the section starting with "3. Trading volume analysis"
            sections = analysis.split("\n\n")
            for section in sections:
                if "volume analysis" in section.lower():
                    return section.strip()
            # If not found, return the first paragraph after "3."
            for section in sections:
                if section.strip().startswith("3."):
                    return section.strip()
            return "Volume analysis not found"
        except Exception:
            return "Error extracting volume analysis"

    async def process_stock_data(self, ticker: str, date: str) -> dict:
        """Process stock data through the workflow."""
        try:
            initial_state = {
                "ticker": ticker,
                "date": date,
                "raw_data": None,
                "enhanced_data": None,
                "final_data": None
            }
            
            result = await self.workflow.ainvoke(initial_state)
            return result["final_data"]
        except Exception as e:
            logger.error(f"Error processing stock data: {e}")
            raise