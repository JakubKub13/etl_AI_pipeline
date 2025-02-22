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
from ...db.models import StockStatus, MarketSentiment

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
            logger.info(f"Raw data fetched for {state['ticker']}")
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
            1. Overall market sentiment (explicitly state if bullish, bearish, or neutral)
            2. Detailed price movement analysis
            3. Trading volume analysis and its significance
            4. Comprehensive summary of the day's trading activity
            """

            response = await self.anthropic.ainvoke(input=prompt)

            analysis = response.content
            print("Analysis:", analysis)
            
            # Extract sentiment with proper validation
            sentiment = self._extract_sentiment(analysis)
            if not isinstance(sentiment, MarketSentiment):
                sentiment = MarketSentiment.NEUTRAL
                logger.warning(f"Invalid sentiment detected, defaulting to {sentiment}")

            enhanced_data = {
                "llm_analysis": analysis,
                "market_sentiment": sentiment.value,
                "price_movement_summary": self._extract_price_analysis(analysis),
                "trading_volume_analysis": self._extract_volume_analysis(analysis)
            }
            
            logger.info(f"Enhanced data generated for {raw_data.ticker}")
            return {"enhanced_data": enhanced_data}
        except Exception as e:
            logger.error(f"Error in LLM enhancement: {e}")
            raise

    async def save_to_database(self, state: StockDataState) -> dict:
        """Save both raw and enhanced data to database."""
        try:
            raw_data = state["raw_data"]
            enhanced_data = state["enhanced_data"]
            
            # Save both stock data and analysis
            stock_data, analysis = await self.stock_data_manager.save_stock_data_with_analysis(
                stock_data=raw_data,
                analysis_data=enhanced_data
            )
            
            logger.info(f"Data saved successfully for {raw_data.ticker}")
            return {
                "final_data": {
                    "stock_data": stock_data,
                    "analysis": analysis
                }
            }
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            raise

    @staticmethod
    def _extract_sentiment(analysis: str) -> MarketSentiment:
        """Extract and validate market sentiment from analysis."""
        analysis_lower = analysis.lower()
        if "bullish" in analysis_lower:
            return MarketSentiment.BULLISH
        elif "bearish" in analysis_lower:
            return MarketSentiment.BEARISH
        return MarketSentiment.NEUTRAL

    @staticmethod
    def _extract_price_analysis(analysis: str) -> str:
        """Extract price movement analysis with validation."""
        try:
            sections = analysis.split("\n\n")
            for section in sections:
                if "price movement" in section.lower():
                    return section.strip()
            # Fallback to numbered section
            for section in sections:
                if section.strip().startswith("2."):
                    return section.strip()
            return "Price analysis not available"
        except Exception as e:
            logger.error(f"Error extracting price analysis: {e}")
            return "Error in price analysis extraction"

    @staticmethod
    def _extract_volume_analysis(analysis: str) -> str:
        """Extract volume analysis with validation."""
        try:
            sections = analysis.split("\n\n")
            for section in sections:
                if "volume" in section.lower():
                    return section.strip()
            # Fallback to numbered section
            for section in sections:
                if section.strip().startswith("3."):
                    return section.strip()
            return "Volume analysis not available"
        except Exception as e:
            logger.error(f"Error extracting volume analysis: {e}")
            return "Error in volume analysis extraction"

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
            logger.info(f"Successfully processed data for {ticker}")
            return result["final_data"]
        except Exception as e:
            logger.error(f"Error processing stock data: {e}")
            raise