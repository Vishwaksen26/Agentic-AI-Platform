"""Authentication dependencies for FastAPI."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.auth.security import decode_token

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Extract and validate the current user from the JWT token.
    
    Args:
        credentials: HTTP bearer credentials from the request
        
    Returns:
        dict: Decoded token payload containing user information
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {"user_id": user_id, **payload}
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """
    Extract current user from JWT token if present, otherwise return None.
    """
    if not credentials:
        return None
    
    return await get_current_user(credentials)


async def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Ensure the current user has admin role.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


async def require_role(*roles: str):
    """
    Factory function to create a dependency that requires one of multiple roles.
    """
    async def check_role(current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("role")
        
        if user_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access requires one of roles: {', '.join(roles)}"
            )
        
        return current_user
    
    return check_role
