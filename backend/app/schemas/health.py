"""
Pydantic schemas for API health check endpoints.
Fully compliant with Pydantic v2.
"""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """General API health response."""

    status: str = Field(..., json_schema_extra={"example": "healthy"})
    version: str = Field(..., json_schema_extra={"example": "1.0.0"})
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    environment: str = Field(..., json_schema_extra={"example": "development"})


class DatabaseHealthResponse(BaseModel):
    """Database connectivity health response."""

    status: str = Field(..., json_schema_extra={"example": "healthy"})
    database: str = Field(..., json_schema_extra={"example": "connected"})
    dialect: Optional[str] = Field(None, json_schema_extra={"example": "postgresql"})
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error: Optional[str] = Field(None, json_schema_extra={"example": None})
