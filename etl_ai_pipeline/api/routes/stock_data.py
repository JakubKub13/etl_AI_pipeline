from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from pydantic import BaseModel
import logging

from ...agent.data_retrieval_workflow.data_retrieval_graph import DataRetrievalGraph
from ...api.models.models import StockDataRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stock-data", tags=["Stock Data"])

@router.post(
    "/process",
    summary="Process Stock Data",
    description="Fetch, enhance, and store stock data for a given ticker and date"
)
async def process_stock_data(request: StockDataRequest):
    """
    Process stock data through the LangGraph workflow.
    
    Args:
        request (StockDataRequest): Stock data request parameters
        
    Returns:
        dict: Processed and enhanced stock data
    """
    try:
        workflow = DataRetrievalGraph()
        result = await workflow.process_stock_data(
            request.ticker,
            request.date
        )
        return result
    except Exception as e:
        logger.error(f"Error processing stock data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

