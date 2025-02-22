from fastapi import APIRouter, HTTPException
from typing import Optional
from ...db.analysis_queries import StockAnalyzer
from ...db.Stock_data_manager import StockDataManager


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