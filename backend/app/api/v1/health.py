"""
Health check endpoints for API and Database connectivity.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import check_db_connection
from app.schemas.health import HealthResponse, DatabaseHealthResponse

router = APIRouter()


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="API Health Status",
    description="Returns the operational status, version, environment, and current timestamp of the Elevate X AI API.",
)
async def get_health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.now(timezone.utc),
        environment=settings.APP_ENV,
    )


@router.head("", include_in_schema=False)
async def head_health():
    return None


@router.get(
    "/database",
    response_model=DatabaseHealthResponse,
    responses={
        200: {
            "description": "Database is connected and healthy",
            "model": DatabaseHealthResponse,
        },
        503: {
            "description": "Database connection failed or is unreachable",
            "model": DatabaseHealthResponse,
        },
    },
    summary="Database Connectivity Check",
    description="Tests actual database connectivity by executing a lightweight query on PostgreSQL.",
)
async def get_database_health():
    is_connected, dialect, error_msg = check_db_connection()

    if is_connected:
        return DatabaseHealthResponse(
            status="healthy",
            database="connected",
            dialect=dialect,
            timestamp=datetime.now(timezone.utc),
            error=None,
        )
    else:
        # Strictly return 503 Service Unavailable when DB is unreachable
        response_content = DatabaseHealthResponse(
            status="unhealthy",
            database="disconnected",
            dialect=None,
            timestamp=datetime.now(timezone.utc),
            error=error_msg or "Failed to connect to database server",
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=response_content.model_dump(mode="json"),
        )

