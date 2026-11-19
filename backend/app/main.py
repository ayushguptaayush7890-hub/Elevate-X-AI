"""
Elevate X AI - Main FastAPI Application Entrypoint.
Configures middleware, CORS, routers, exception handlers, and lifespan lifecycle.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import register_exception_handlers
from app.core.database import check_db_connection
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    Handles startup configuration checks and graceful shutdown.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} [{settings.APP_ENV}]")
    logger.info(f"CORS Allowed Origins: {settings.CORS_ORIGINS}")
    
    # Test initial database connectivity
    db_connected, dialect, err = check_db_connection()
    if db_connected:
        logger.info(f"Database connected successfully via dialect '{dialect}'.")
        try:
            from app.core.database import Base, engine
            Base.metadata.create_all(bind=engine)
            logger.info("Database schemas verified and updated.")
        except Exception as ex:
            logger.warning(f"Schema initialization warning: {ex}")
    else:
        logger.warning(
            f"Database connectivity test at startup failed ({err}). "
            "Ensure PostgreSQL is running locally or via Docker."
        )

    yield

    logger.info(f"Shutting down {settings.APP_NAME}.")


# FastAPI Application Instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Elevate X AI – AI-Powered Vocational Career & Skills Ecosystem API. "
        "Provides backend services for trade skill recognition, assessment diagnostics, and job matching."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# 1. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Centralized Exception Handlers
register_exception_handlers(app)

# 3. Mount Modular API Routers
# Primary v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
# Convenience alias for frontend compatibility
app.include_router(api_router, prefix="/api")


@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirects root to the Swagger documentation."""
    return RedirectResponse(url="/docs")

