"""
EduPath FastAPI Backend Main Entrypoint.

Configures application lifecycle, database initialization, CORS, global error handling,
and API version 1 routing.
"""

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

from starlette.exceptions import HTTPException as StarletteHTTPException

# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Preserves HTTP status code and detail for intentional HTTPExceptions (e.g., 404, 400, 401, 503)."""
    detail_msg = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": detail_msg,
            "error": {
                "code": "NOT_FOUND" if exc.status_code == 404 else ("UNAUTHORIZED" if exc.status_code == 401 else "HTTP_ERROR"),
                "message": detail_msg,
                "path": str(request.url.path),
            }
        },
    )



@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Centralized exception handler providing structured JSON error responses for unexpected server errors."""
    logger.error(f"Unhandled Server Error on {request.method} {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred on the server.",
                "path": str(request.url.path),
            }
        },
    )



@app.get("/")
async def root():
    """Root application endpoint redirecting to health check and docs."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
    }
