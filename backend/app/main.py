"""
Backend Service - Main FastAPI Application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.v1.endpoints import health

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print(f"🚀 Starting backend server on {settings.API_HOST}:{settings.API_PORT}")
    print(f"📊 Database: {settings.DB_NAME}")
    yield
    # Shutdown
    print("🛑 Shutting down backend server")


# Create FastAPI app
app = FastAPI(
    title="For.Ever Cosmetics CRM API",
    description="Backend API for Telegram Mini App CRM",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENABLE_SWAGGER else None,
    redoc_url="/redoc" if settings.ENABLE_SWAGGER else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "For.Ever Cosmetics CRM API",
        "version": "0.1.0",
        "docs": "/docs"
    }
