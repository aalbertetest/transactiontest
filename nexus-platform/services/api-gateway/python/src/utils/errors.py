# =============================================================================
# NEXUS PLATFORM - API GATEWAY - ERROR DEFINITIONS
# =============================================================================
# Custom exception classes for API error handling.
# =============================================================================

"""
Error Module

This module defines custom exception classes for the API Gateway.
These exceptions are caught by error handlers and converted to
appropriate HTTP responses.

Error Hierarchy:
- APIError (base class)
  - AuthenticationError (401)
  - AuthorizationError (403)
  - NotFoundError (404)
  - ValidationError (422)
  - RateLimitExceeded (429)
  - ServiceUnavailable (503)
"""

from typing import Any, Dict, List, Optional


class APIError(Exception):
    """
    Base class for all API errors.
    
    This is the base exception for all API-related errors.
    Subclasses should define appropriate status codes and error codes.
    
    Attributes:
        message: Human-readable error message.
        code: Machine-readable error code.
        status_code: HTTP status code.
        details: Additional error details.
    """
    
    status_code: int = 500
    code: str = "INTERNAL_ERROR"
    
    def __init__(
        self,
        message: str = "An unexpected error occurred",
        code: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the API error.
        
        Args:
            message: Human-readable error message.
            code: Machine-readable error code (overrides class default).
            status_code: HTTP status code (overrides class default).
            details: Additional error details.
        """
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.code
        self.status_code = status_code or self.__class__.status_code
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert error to dictionary representation.
        
        Returns:
            Dict: Error as dictionary for JSON serialization.
        """
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }
    
    def __str__(self) -> str:
        """String representation of the error."""
        return f"[{self.code}] {self.message}"
    
    def __repr__(self) -> str:
        """Detailed representation for debugging."""
        return f"{self.__class__.__name__}(code={self.code!r}, message={self.message!r}, status_code={self.status_code})"


class AuthenticationError(APIError):
    """
    Authentication error (401 Unauthorized).
    
    Raised when authentication fails or is required but not provided.
    
    Examples:
        - Missing authentication token
        - Invalid or expired token
        - Invalid credentials
    """
    
    status_code = 401
    code = "AUTHENTICATION_ERROR"
    
    def __init__(
        self,
        message: str = "Authentication required",
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            code=code,
            status_code=401,
            details=details,
        )


class AuthorizationError(APIError):
    """
    Authorization error (403 Forbidden).
    
    Raised when the user is authenticated but lacks permission
    for the requested action.
    
    Examples:
        - Insufficient role
        - Missing required permission
        - Resource access denied
    """
    
    status_code = 403
    code = "AUTHORIZATION_ERROR"
    
    def __init__(
        self,
        message: str = "Permission denied",
        code: Optional[str] = None,
        required_permission: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        details = details or {}
        if required_permission:
            details["required_permission"] = required_permission
        
        super().__init__(
            message=message,
            code=code,
            status_code=403,
            details=details,
        )


class NotFoundError(APIError):
    """
    Resource not found error (404 Not Found).
    
    Raised when a requested resource does not exist.
    
    Examples:
        - User not found
        - Record not found
        - Endpoint not found
    """
    
    status_code = 404
    code = "NOT_FOUND"
    
    def __init__(
        self,
        message: str = "Resource not found",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        details = details or {}
        if resource_type:
            details["resource_type"] = resource_type
        if resource_id:
            details["resource_id"] = resource_id
        
        # Build helpful message if resource info provided
        if resource_type and resource_id:
            message = f"{resource_type} with ID '{resource_id}' not found"
        elif resource_type:
            message = f"{resource_type} not found"
        
        super().__init__(
            message=message,
            code=code,
            status_code=404,
            details=details,
        )


class ValidationError(APIError):
    """
    Validation error (422 Unprocessable Entity).
    
    Raised when request data fails validation.
    
    Attributes:
        field_errors: List of field-specific validation errors.
    
    Examples:
        - Missing required field
        - Invalid field format
        - Value out of range
    """
    
    status_code = 422
    code = "VALIDATION_ERROR"
    
    def __init__(
        self,
        message: str = "Validation failed",
        field_errors: Optional[List[Dict[str, str]]] = None,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        details = details or {}
        if field_errors:
            details["field_errors"] = field_errors
        
        super().__init__(
            message=message,
            code=code,
            status_code=422,
            details=details,
        )
        
        self.field_errors = field_errors or []
    
    @classmethod
    def from_field_error(
        cls,
        field: str,
        message: str,
        error_type: str = "invalid",
    ) -> "ValidationError":
        """
        Create a validation error for a single field.
        
        Args:
            field: Field name that failed validation.
            message: Error message for the field.
            error_type: Type of validation error.
        
        Returns:
            ValidationError: The validation error instance.
        """
        return cls(
            message=f"Validation failed for field '{field}'",
            field_errors=[{
                "field": field,
                "message": message,
                "type": error_type,
            }],
        )


class RateLimitExceeded(APIError):
    """
    Rate limit exceeded error (429 Too Many Requests).
    
    Raised when the client has exceeded their rate limit.
    
    Attributes:
        limit: The rate limit that was exceeded.
        window: The time window for the limit.
        retry_after: Seconds until the client can retry.
        reset_at: Unix timestamp when the limit resets.
    """
    
    status_code = 429
    code = "RATE_LIMIT_EXCEEDED"
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        limit: int = 0,
        window: str = "60s",
        retry_after: int = 60,
        reset_at: int = 0,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.limit = limit
        self.window = window
        self.retry_after = retry_after
        self.reset_at = reset_at
        
        details = details or {}
        details.update({
            "limit": limit,
            "window": window,
            "retry_after": retry_after,
            "reset_at": reset_at,
        })
        
        super().__init__(
            message=message,
            code=code,
            status_code=429,
            details=details,
        )


class ServiceUnavailable(APIError):
    """
    Service unavailable error (503 Service Unavailable).
    
    Raised when a backend service is unavailable, typically
    due to circuit breaker being open.
    
    Attributes:
        service: Name of the unavailable service.
        retry_after: Suggested retry delay in seconds.
    """
    
    status_code = 503
    code = "SERVICE_UNAVAILABLE"
    
    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        service: str = "unknown",
        retry_after: int = 30,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.service = service
        self.retry_after = retry_after
        
        details = details or {}
        details.update({
            "service": service,
            "retry_after": retry_after,
        })
        
        if service != "unknown":
            message = f"Service '{service}' is temporarily unavailable"
        
        super().__init__(
            message=message,
            code=code,
            status_code=503,
            details=details,
        )


class ConflictError(APIError):
    """
    Conflict error (409 Conflict).
    
    Raised when there's a conflict with the current state,
    such as duplicate resources or concurrent modifications.
    
    Examples:
        - Email already registered
        - Optimistic locking failure
        - Duplicate resource creation
    """
    
    status_code = 409
    code = "CONFLICT"
    
    def __init__(
        self,
        message: str = "Resource conflict",
        resource_type: Optional[str] = None,
        conflicting_field: Optional[str] = None,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        details = details or {}
        if resource_type:
            details["resource_type"] = resource_type
        if conflicting_field:
            details["conflicting_field"] = conflicting_field
        
        super().__init__(
            message=message,
            code=code,
            status_code=409,
            details=details,
        )


class BadRequestError(APIError):
    """
    Bad request error (400 Bad Request).
    
    Raised when the request is malformed or cannot be processed.
    
    Examples:
        - Invalid JSON
        - Missing required parameters
        - Invalid parameter values
    """
    
    status_code = 400
    code = "BAD_REQUEST"
    
    def __init__(
        self,
        message: str = "Bad request",
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            code=code,
            status_code=400,
            details=details,
        )


class TimeoutError(APIError):
    """
    Request timeout error (504 Gateway Timeout).
    
    Raised when a request to an upstream service times out.
    """
    
    status_code = 504
    code = "TIMEOUT"
    
    def __init__(
        self,
        message: str = "Request timed out",
        service: Optional[str] = None,
        timeout: Optional[float] = None,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        details = details or {}
        if service:
            details["service"] = service
            message = f"Request to '{service}' timed out"
        if timeout:
            details["timeout"] = timeout
        
        super().__init__(
            message=message,
            code=code,
            status_code=504,
            details=details,
        )
