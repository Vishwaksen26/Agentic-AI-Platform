"""Custom exceptions for the application."""

from typing import Any, Optional


class AppException(Exception):
    """Base exception for the application."""
    
    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
            details=details
        )


class NotFoundError(AppException):
    """Raised when a resource is not found."""
    
    def __init__(self, resource: str, identifier: str):
        message = f"{resource} not found: {identifier}"
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404
        )


class UnauthorizedError(AppException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401
        )


class ForbiddenError(AppException):
    """Raised when user lacks permissions."""
    
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=403
        )


class ConflictError(AppException):
    """Raised when there is a conflict (e.g., duplicate resource)."""
    
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=409
        )


class RateLimitError(AppException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            code="RATE_LIMIT",
            status_code=429
        )


class InternalServerError(AppException):
    """Raised for internal server errors."""
    
    def __init__(self, message: str = "Internal server error", details: Optional[dict] = None):
        super().__init__(
            message=message,
            code="INTERNAL_ERROR",
            status_code=500,
            details=details
        )
