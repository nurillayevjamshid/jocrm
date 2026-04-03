"""
Backend API - Simple FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.api.health import router as health_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    print(f"🚀 Backend starting on {settings.API_HOST}:{settings.API_PORT}")
    yield
    print("🛑 Backend shutting down")


app = FastAPI(
    title="For.Ever Cosmetics CRM API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENABLE_SWAGGER else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/health", tags=["health"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "For.Ever Cosmetics CRM API",
        "version": "0.1.0",
        "docs": "/docs"
    }
