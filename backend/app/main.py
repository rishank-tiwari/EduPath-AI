"""
EduPath FastAPI Backend Main Entrypoint.

Configures application lifecycle, database initialization, CORS, global error handling,
and API version 1 routing.
"""

import traceback
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.api.router import api_router
from app.core.config import settings
from app.core.database import close_mongo_connection, connect_to_mongo
from app.middleware.cors import setup_cors
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown event handlers."""
    logger.info("Initializing EduPath API backend...")
    connect_to_mongo()
    yield
    logger.info("Shutting down EduPath API backend...")
    close_mongo_connection()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="EduPath — AI-powered adaptive career learning companion REST API.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Setup CORS
setup_cors(app)

# Include API v1 router with both /api/v1 prefix and v1 prefix for serverless routing flexibility
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(api_router, prefix="/v1")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Centralized exception handler providing structured JSON error responses."""
    err_msg = str(exc) or exc.__class__.__name__
    logger.error(f"Unhandled Server Error on {request.method} {request.url.path}: {err_msg}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": err_msg,
                "path": str(request.url.path),
            }
        },
    )


@app.get("/")
@app.get("/api")
@app.get("/health")
async def root():
    """Root application endpoint redirecting to health check and status."""
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
    }
