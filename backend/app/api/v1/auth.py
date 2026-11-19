"""
Authentication API Endpoints (Registration, Login, Token Management, Password Reset).
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets
import uuid
import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.config import settings
from app.core.database import get_db
from app.core.logging import logger
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_secure_token,
)
from app.models.user import User, PasswordResetToken, RevokedToken
from app.models.profile import UserProfile
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    TokenRefreshRequest,
    UserResponse,
    AuthResponse,
    PasswordChangeRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    MessageResponse,
)
from app.api.deps import get_current_user, oauth2_scheme

router = APIRouter()


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New User",
    description="Registers a new user account with hashed password and auto-initializes their vocational profile.",
)
async def register(
    payload: UserRegisterRequest,
    db: Session = Depends(get_db),
):
    # Check duplicate email
    existing = db.execute(
        select(User).where(User.email == payload.email.lower().strip())
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists.",
        )

    # Create User
    new_user = User(
        email=payload.email.lower().strip(),
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role="user",
        is_active=True,
        is_verified=False,
    )
    db.add(new_user)
    db.flush()

    # Create Initial Vocational Profile
    new_profile = UserProfile(
        user_id=new_user.id,
        headline=f"{payload.trade_category or 'Vocational Artisan'} Professional",
        trade_category=payload.trade_category,
        completion_percentage=25,
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_user)

    # Generate JWT Tokens
    token_claims = {"role": new_user.role, "jti": secrets.token_hex(16)}
    access_token = create_access_token(subject=str(new_user.id), claims=token_claims)
    refresh_token = create_refresh_token(subject=str(new_user.id))

    return AuthResponse(
        token=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ),
        user=UserResponse.model_validate(new_user),
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Authenticate User",
    description="Authenticates user credentials and returns JWT access & refresh tokens.",
)
async def login(
    payload: UserLoginRequest,
    db: Session = Depends(get_db),
):
    user = db.execute(
        select(User).where(User.email == payload.email.lower().strip())
    ).scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Contact support.",
        )

    token_claims = {"role": user.role, "jti": secrets.token_hex(16)}
    access_token = create_access_token(subject=str(user.id), claims=token_claims)
    refresh_token = create_refresh_token(subject=str(user.id))

    return AuthResponse(
        token=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ),
        user=UserResponse.model_validate(user),
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get Current User",
    description="Returns profile information for the currently authenticated bearer token user.",
)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Log Out User",
    description="Revokes the active bearer JWT token by tracking its unique identifier in the token blacklist.",
)
async def logout(
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_token(token)
        jti = payload.get("jti")
        exp_ts = payload.get("exp")
        exp_dt = (
            datetime.fromtimestamp(exp_ts, timezone.utc)
            if exp_ts
            else datetime.now(timezone.utc) + timedelta(days=1)
        )

        if jti:
            revocation = RevokedToken(jti=jti, expires_at=exp_dt)
            db.add(revocation)
            db.commit()
    except Exception as exc:
        logger.warning(f"Logout token tracking warning: {exc}")

    return MessageResponse(success=True, message="Successfully logged out.")


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh Access Token",
    description="Issues a fresh JWT access token using a valid refresh token.",
)
async def refresh_token(
    payload: TokenRefreshRequest,
    db: Session = Depends(get_db),
):
    try:
        data = decode_token(payload.refresh_token)
        if data.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type for refresh",
            )
        user_id_str = data.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token payload",
            )
        user_uuid = uuid.UUID(user_id_str)
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user = db.execute(select(User).where(User.id == user_uuid)).scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    new_access_token = create_access_token(
        subject=str(user.id),
        claims={"role": user.role, "jti": secrets.token_hex(16)},
    )
    new_refresh_token = create_refresh_token(subject=str(user.id))

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    summary="Initiate Password Recovery",
    description="Generates a secure password reset token for the requested email account.",
)
async def forgot_password(
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    user = db.execute(
        select(User).where(User.email == payload.email.lower().strip())
    ).scalar_one_or_none()

    # Always return a generic success message to prevent user enumeration attacks
    if not user:
        return MessageResponse(
            success=True,
            message="If this email exists in our records, password reset instructions have been generated.",
        )

    reset_token = generate_secure_token(48)
    expires_at = datetime.now(timezone.utc) + timedelta(
        hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS
    )

    token_record = PasswordResetToken(
        user_id=user.id,
        token=reset_token,
        expires_at=expires_at,
        is_used=False,
    )
    db.add(token_record)
    db.commit()

    # In development mode, log the reset token for direct workflow testing
    logger.info(
        f"[AUTH] Password reset token generated for user {user.email}: token={reset_token} (expires at {expires_at})"
    )

    return MessageResponse(
        success=True,
        message="If this email exists in our records, password reset instructions have been generated.",
        details={"token_preview": reset_token if settings.DEBUG else None},
    )


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    summary="Complete Password Reset",
    description="Resets the user's password using the issued reset token.",
)
async def reset_password(
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    token_record = db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.token == payload.token,
            PasswordResetToken.is_used == False,
        )
    ).scalar_one_or_none()

    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or already used password reset token.",
        )

    expires_at = token_record.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset token has expired. Please request a new one.",
        )

    user = db.execute(select(User).where(User.id == token_record.user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.hashed_password = hash_password(payload.new_password)
    token_record.is_used = True
    db.commit()

    logger.info(f"[AUTH] Password reset completed successfully for user {user.email}")
    return MessageResponse(
        success=True,
        message="Your password has been reset successfully. You may now log in with your new credentials.",
    )


@router.post(
    "/change-password",
    response_model=MessageResponse,
    summary="Change Password",
    description="Changes password for the currently logged in user after verifying current password.",
)
async def change_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    current_user.hashed_password = hash_password(payload.new_password)
    db.commit()

    return MessageResponse(success=True, message="Password updated successfully.")

