from fastapi import APIRouter, HTTPException
from typing import Optional
from ...db.analysis_queries import StockAnalyzer
from ...db.Stock_data_manager import StockDataManager
from ...agent.agent_workflow.stock_analysis_agent import StockAnalysisAgent
from ...api.models.models import StockAnalysisRequest
from ...agent.models import EmailConfig
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/volatility/{ticker}")
async def get_short_term_volatility(ticker: str):
    """
    Získa 3-dňovú volatilitu pre daný ticker.
    
    - **ticker**: Symbol akcie (napr. MSFT, AAPL)
    """
    try:
        analyzer = StockAnalyzer(StockDataManager())
        return await analyzer.calculate_short_term_volatility(ticker)
    except Exception as e:
        print(f"Error calculating volatility: {e}") 
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends/{ticker}")
async def get_short_term_trends(ticker: str):
    """
    Získa krátkodobú analýzu trendov pre daný ticker.
    
    - **ticker**: Symbol akcie (napr. MSFT, AAPL)
    """
    try:
        analyzer = StockAnalyzer(StockDataManager())
        return await analyzer.identify_short_term_trends(ticker)
    except Exception as e:
        print(f"Error identifying trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# Add new endpoint
@router.post("/stock-analysis")
async def run_stock_analysis(request: StockAnalysisRequest):
    """Run complete stock analysis and send email report."""
    try:
        agent = StockAnalysisAgent()
        email_config = EmailConfig(
            recipient_email=request.email_config.recipient_email,
            subject=request.email_config.subject,
            cc=request.email_config.cc
        )
        
        result = await agent.run_analysis(
            ticker=request.ticker,
            date=datetime.now().strftime("%Y-%m-%d"),
            email_config=email_config
        )
        
        return {
            "status": "success",
            "ticker": request.ticker,
            "email_sent": result.get("email_sent", False)
        }
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))