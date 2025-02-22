import asyncio
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
import uvicorn
from datetime import datetime

from .settings import settings
from .api.routes import health, stock_data, analysis
from .api.dependencies.auth import verify_api_key
from .api.models.models import ErrorResponse

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    dependencies=[Depends(verify_api_key)]
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

# Include routers
app.include_router(health.router)
app.include_router(stock_data.router)
app.include_router(analysis.router)

async def start_app():
    """Async entry point for the application."""
    config = uvicorn.Config(
        "etl_ai_pipeline.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        loop="asyncio",
        workers=settings.WORKERS if hasattr(settings, 'WORKERS') else 4
    )
    server = uvicorn.Server(config)
    await server.serve()

def start():
    """Synchronous entry point for Poetry."""
    try:
        asyncio.run(start_app())
    except KeyboardInterrupt:
        logger.info("Server shutting down...")

if __name__ == "__main__":
    start()