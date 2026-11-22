"""
FastAPI Dependencies for Authentication, Database Sessions, and Profile Resolution.
"""

from typing import Generator, Optional
import uuid
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User, RevokedToken
from app.models.profile import UserProfile

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=True,
)

oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=False,
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Decodes bearer token, verifies revocation status, and retrieves the authenticated User.
    Raises 401 Unauthorized on invalid/expired tokens.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        user_id_str: str = payload.get("sub")
        token_type: str = payload.get("type", "access")
        jti: str = payload.get("jti")

        if user_id_str is None or token_type != "access":
            raise credentials_exception

        user_id = uuid.UUID(user_id_str)
    except (jwt.PyJWTError, ValueError):
        raise credentials_exception

    # Check if token JTI has been revoked
    if jti:
        revoked = db.execute(
            select(RevokedToken).where(RevokedToken.jti == jti)
        ).scalar_one_or_none()
        if revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Ensures current user is active."""
    return current_user


def require_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Ensures the authenticated user has administrative privileges."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required for this action.",
        )
    return current_user


def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> UserProfile:
    """
    Retrieves the UserProfile belonging to the authenticated user.
    Creates an initial profile if one was not created during registration.
    """
    profile = db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    ).scalar_one_or_none()

    if profile is None:
        profile = UserProfile(
            user_id=current_user.id,
            headline=f"{current_user.full_name or 'Artisan'} Professional Profile",
            completion_percentage=25,
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    Attempts to decode bearer token and retrieve User.
    Returns None if token is absent, invalid, or expired without throwing 401.
    """
    if not token:
        return None

    try:
        payload = decode_token(token)
        user_id_str: str = payload.get("sub")
        token_type: str = payload.get("type", "access")
        jti: str = payload.get("jti")

        if user_id_str is None or token_type != "access":
            return None

        user_id = uuid.UUID(user_id_str)

        if jti:
            revoked = db.execute(
                select(RevokedToken).where(RevokedToken.jti == jti)
            ).scalar_one_or_none()
            if revoked:
                return None

        user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
        if user and user.is_active:
            return user
    except Exception:
        return None

    return None

