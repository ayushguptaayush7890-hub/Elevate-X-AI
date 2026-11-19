"""
Pydantic v2 schemas for Authentication, Registration, and Password workflows.
"""

from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """User registration payload."""

    email: EmailStr = Field(..., description="Valid user email address")
    password: str = Field(..., min_length=6, max_length=128, description="Strong user password")
    full_name: Optional[str] = Field(None, max_length=255, description="Full display name")
    trade_category: Optional[str] = Field(None, description="Optional primary vocational trade")


class UserLoginRequest(BaseModel):
    """User login payload."""

    email: EmailStr = Field(..., description="Registered user email")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    """Authentication tokens returned on successful login or register."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Access token expiration in seconds")


class TokenRefreshRequest(BaseModel):
    """Payload to request a new access token using a refresh token."""

    refresh_token: str


class UserResponse(BaseModel):
    """Safe user profile response without password hashes."""

    id: uuid.UUID
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuthResponse(BaseModel):
    """Unified response containing tokens and basic user profile."""

    token: TokenResponse
    user: UserResponse


class PasswordChangeRequest(BaseModel):
    """Authenticated password update payload."""

    current_password: str
    new_password: str = Field(..., min_length=6, max_length=128)


class ForgotPasswordRequest(BaseModel):
    """Request payload to initiate password reset."""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Payload to complete password reset using issued token."""

    token: str
    new_password: str = Field(..., min_length=6, max_length=128)


class MessageResponse(BaseModel):
    """Generic status or success notification message."""

    success: bool = True
    message: str
    details: Optional[dict] = None

