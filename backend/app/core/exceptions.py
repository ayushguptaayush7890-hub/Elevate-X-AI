"""
Custom application exceptions and centralized FastAPI exception handlers.
"""

from typing import Any, Dict, Optional
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.core.logging import logger
from app.core.config import settings


# -----------------------------------------------------------------------------
# Base & Domain Exceptions
# -----------------------------------------------------------------------------

class ElevateXException(Exception):
    """Base class for all Elevate X application exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class DatabaseConnectionException(ElevateXException):
    """Raised when the database connection fails or is unreachable."""

    def __init__(self, message: str = "Database connection unavailable", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details,
        )


class EntityNotFoundException(ElevateXException):
    """Raised when a requested resource is not found."""

    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            message=f"{entity_name} with identifier '{entity_id}' was not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"entity": entity_name, "id": str(entity_id)},
        )


# -----------------------------------------------------------------------------
# Centralized Handlers Registration
# -----------------------------------------------------------------------------

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ElevateXException)
    async def elevate_x_exception_handler(request: Request, exc: ElevateXException) -> JSONResponse:
        logger.error(f"Application error at {request.url.path}: {exc.message} (status={exc.status_code})")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.__class__.__name__,
                    "message": exc.message,
                    "details": exc.details,
                },
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        logger.warning(f"HTTP {exc.status_code} at {request.url.path}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": "HTTPException",
                    "message": str(exc.detail),
                },
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning(f"Validation error at {request.url.path}: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "ValidationError",
                    "message": "Input validation failed",
                    "details": exc.errors(),
                },
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        logger.error(f"Database error at {request.url.path}: {str(exc)}")
        message = str(exc) if settings.DEBUG else "A database error occurred."
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "DatabaseError",
                    "message": message,
                },
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.critical(f"Unhandled exception at {request.url.path}: {str(exc)}", exc_info=True)
        message = str(exc) if settings.DEBUG else "An unexpected internal server error occurred."
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "InternalServerError",
                    "message": message,
                },
            },
        )

