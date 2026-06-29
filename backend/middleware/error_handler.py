"""Middleware for the FastAPI application."""

import logging
import time
import json
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.exceptions.handlers import AppException
from backend.schemas.base import ErrorResponse


logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for handling exceptions and converting them to proper responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except AppException as exc:
            error_response = ErrorResponse(
                code=exc.code,
                message=exc.message,
                details=exc.details,
                status_code=exc.status_code
            )
            
            logger.warning(
                f"AppException: {exc.code} - {exc.message}",
                extra={"details": exc.details}
            )
            
            return JSONResponse(
                status_code=exc.status_code,
                content=error_response.dict()
            )
        except Exception as exc:
            logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
            
            error_response = ErrorResponse(
                code="INTERNAL_ERROR",
                message="An internal server error occurred",
                status_code=500
            )
            
            return JSONResponse(
                status_code=500,
                content=error_response.dict()
            )


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip logging for health check endpoints
        if request.url.path == "/health":
            return await call_next(request)
        
        start_time = time.time()
        
        # Log request
        logger.info(
            f"{request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
            }
        )
        
        response = await call_next(request)
        
        # Calculate request duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            }
        )
        
        return response


class CORSHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware for adding CORS headers."""
    
    def __init__(self, app, allow_origins=None, allow_methods=None, allow_headers=None):
        super().__init__(app)
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["*"]
        self.allow_headers = allow_headers or ["*"]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.method == "OPTIONS":
            return Response(
                headers={
                    "Access-Control-Allow-Origin": ", ".join(self.allow_origins),
                    "Access-Control-Allow-Methods": ", ".join(self.allow_methods),
                    "Access-Control-Allow-Headers": ", ".join(self.allow_headers),
                }
            )
        
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = ", ".join(self.allow_origins)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware for adding security headers."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response
