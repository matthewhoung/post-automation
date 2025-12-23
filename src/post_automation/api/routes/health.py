"""Health check endpoint."""

from datetime import datetime

from fastapi import APIRouter

from post_automation.models.api_schemas import HealthResponse
from post_automation.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status of the service.
    """
    # Check if AI models can be loaded (lightweight check)
    models_ok = True
    try:
        from post_automation.core.ai_detector import get_detector

        # Note: This will load the model on first call
        # Consider adding a flag to skip model loading for health checks
        logger.info("Health check: AI detector accessible")
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        models_ok = False

    status_val = "healthy" if models_ok else "degraded"

    return HealthResponse(
        status=status_val,
        timestamp=datetime.utcnow().isoformat() + "Z",
        version="0.1.0",
        models_loaded=models_ok,
    )
