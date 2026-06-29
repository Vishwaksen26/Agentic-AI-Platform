"""Authentication routes."""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.base import (
    UserLogin,
    UserRegister,
    UserResponse,
    TokenResponse,
    SuccessResponse,
)
from backend.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=SuccessResponse[UserResponse])
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends()
):
    """Register a new user."""
    # TODO: Implement user registration with database
    # For now, return mock response
    return SuccessResponse(
        data=UserResponse(
            id="1",
            email=user_data.email,
            name=user_data.name,
            role="user",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        )
    )


@router.post("/login", response_model=SuccessResponse[TokenResponse])
async def login(user_data: UserLogin):
    """Login a user and return access token."""
    # TODO: Implement user authentication with database
    # For now, return mock tokens
    
    access_token = create_access_token(
        data={"sub": "1", "email": user_data.email, "role": "user"}
    )
    refresh_token = create_refresh_token("1")
    
    return SuccessResponse(
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=86400,  # 24 hours
        )
    )


@router.post("/refresh", response_model=SuccessResponse[TokenResponse])
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token."""
    # TODO: Implement token refresh
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh not yet implemented"
    )


@router.get("/me", response_model=SuccessResponse[UserResponse])
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information."""
    # TODO: Fetch user from database using current_user["user_id"]
    # For now, return mock response
    return SuccessResponse(
        data=UserResponse(
            id=current_user.get("user_id", "1"),
            email=current_user.get("email", "user@example.com"),
            name=current_user.get("name", "User"),
            role="user",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        )
    )


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout the current user."""
    # TODO: Implement logout (invalidate token)
    return {"message": "Logged out successfully"}
