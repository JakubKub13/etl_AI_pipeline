from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
import logging

from ...settings import settings
from ..models.responses import HealthResponse

# Create router with tags for API documentation
router = APIRouter(
    prefix="/health",
    tags=["System"]
)

logger = logging.getLogger(__name__)

@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API is running and healthy"
)
async def health_check():
    """
    Perform a health check of the system.
    
    Returns:
        HealthResponse: Object containing health status information
    """
    try:
        return HealthResponse(
            status="healthy",
            version=settings.APP_VERSION
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Health check failed"
        )