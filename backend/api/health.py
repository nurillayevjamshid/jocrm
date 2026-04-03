"""
Health check endpoint.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "crm-backend"
    }


@router.get("/ping")
async def ping():
    """Simple ping endpoint."""
    return {"message": "pong"}
