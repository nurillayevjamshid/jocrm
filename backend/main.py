"""
Backend API - Simple FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.api.health import router as health_router
from backend.api.auth import router as auth_router

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

# CORS sozlamalari - Frontend (Mini App) ulanishi uchun
origins = settings.cors_origins_list
# Agar localhost bo'lsa, qo'shimcha variantlarni ham qo'shib qo'yamiz
if "http://localhost:5173" in origins:
    origins.extend(["http://127.0.0.1:5173", "http://0.0.0.0:5173"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print(f"🌍 CORS ruxsat etilgan manzillar: {origins}")

app.include_router(health_router, prefix="/api/health", tags=["health"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "For.Ever Cosmetics CRM API",
        "version": "0.1.0",
        "docs": "/docs"
    }
