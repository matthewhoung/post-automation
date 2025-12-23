"""FastAPI application for post-automation API."""

from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from post_automation.api.routes import detection, health, modification
from post_automation.models.api_schemas import ErrorResponse
from post_automation.utils.config import get_settings
from post_automation.utils.logger import setup_logger

logger = setup_logger(__name__)
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Post Automation API",
    description="AI content detection and PowerPoint modification API for n8n integration",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware for n8n integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(detection.router, prefix="/api", tags=["Detection"])
app.include_router(modification.router, prefix="/api", tags=["Modification"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """Handle all unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            detail=str(exc),
            error_type=type(exc).__name__,
            timestamp=datetime.utcnow().isoformat() + "Z",
        ).dict(),
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Starting Post Automation API")
    logger.info(f"API Host: {settings.api_host}:{settings.api_port}")
    logger.info(f"CORS Origins: {settings.cors_origins_list}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down Post Automation API")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Post Automation API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/health",
    }
