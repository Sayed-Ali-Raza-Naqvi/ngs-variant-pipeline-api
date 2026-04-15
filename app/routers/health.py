from fastapi import APIRouter
from app.models.pipeline import HealthResponse


router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
async def health_check_endpoint():
    """
    Health check endpoint to verify that the API is running.
    """
    return HealthResponse(
        status="ok",
        message="API is healthy and running."
    )