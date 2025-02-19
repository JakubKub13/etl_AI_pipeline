from typing import Optional
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
import uvicorn
from datetime import datetime
import logging

from .settings import settings
from .authorization import BearerAuthenticator
# from .api.models.ollama_models import OllamaRequest, OllamaResponse
# from .api.models.open_router_models import OpenRouterRequest, OpenRouterResponse
# from .api.services.ollama_experimental_endpoint import OllamaService
# from .api.services.open_router_experimental import OpenRouterService

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

authenticator = BearerAuthenticator()

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    dependencies=[Depends(authenticator)]  # Apply token authentication to all routes
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom OpenAPI schema configuration
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description=settings.API_DESCRIPTION,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Pydantic models for request/response validation
class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(..., example=settings.APP_VERSION)

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error"}
    )

# Health check endpoint
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
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

def start():
    """Entry point for the application."""
    uvicorn.run("etl_ai_pipeline.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
