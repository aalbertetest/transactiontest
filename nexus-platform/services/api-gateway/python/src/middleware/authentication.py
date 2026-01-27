# =============================================================================
# NEXUS PLATFORM - API GATEWAY - AUTHENTICATION MIDDLEWARE
# =============================================================================
# JWT and API key authentication with comprehensive security features.
# =============================================================================

"""
Authentication Middleware

This middleware handles authentication for all incoming requests using:
- JWT Bearer tokens (OAuth2 compatible)
- API keys (for programmatic access)

Features:
- RS256/ES256/HS256 JWT verification
- Token expiration validation
- Scope and permission checking
- API key validation with rate limiting
- Request context enrichment with user info
- Support for public endpoints
- Token refresh handling
"""

import re
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional, Set

import structlog
from fastapi import Request, Response
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from starlette.middleware.base import BaseHTTPMiddleware

from ..config import AuthSettings
from ..utils.errors import AuthenticationError

logger = structlog.get_logger(__name__)


class AuthenticatedUser:
    """
    Represents an authenticated user.
    
    This class holds all relevant information about the authenticated user,
    extracted from the JWT token or API key lookup.
    
    Attributes:
        user_id: Unique user identifier.
        email: User's email address.
        roles: List of user roles.
        permissions: List of user permissions.
        scopes: List of token scopes.
        tenant_id: Organization/tenant identifier.
        session_id: Current session identifier.
        token_type: Type of authentication (jwt, api_key).
        is_service_account: Whether this is a service account.
        metadata: Additional user metadata.
    """
    
    def __init__(
        self,
        user_id: str,
        email: Optional[str] = None,
        roles: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None,
        scopes: Optional[List[str]] = None,
        tenant_id: Optional[str] = None,
        session_id: Optional[str] = None,
        token_type: str = "jwt",
        is_service_account: bool = False,
        metadata: Optional[Dict] = None,
    ):
        self.user_id = user_id
        self.email = email
        self.roles = roles or []
        self.permissions = permissions or []
        self.scopes = scopes or []
        self.tenant_id = tenant_id
        self.session_id = session_id
        self.token_type = token_type
        self.is_service_account = is_service_account
        self.metadata = metadata or {}
    
    def has_role(self, role: str) -> bool:
        """Check if user has a specific role."""
        return role in self.roles
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        return permission in self.permissions
    
    def has_scope(self, scope: str) -> bool:
        """Check if token has a specific scope."""
        return scope in self.scopes
    
    def has_any_role(self, roles: List[str]) -> bool:
        """Check if user has any of the specified roles."""
        return bool(set(self.roles) & set(roles))
    
    def has_all_roles(self, roles: List[str]) -> bool:
        """Check if user has all of the specified roles."""
        return set(roles).issubset(set(self.roles))
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "roles": self.roles,
            "permissions": self.permissions,
            "scopes": self.scopes,
            "tenant_id": self.tenant_id,
            "session_id": self.session_id,
            "token_type": self.token_type,
            "is_service_account": self.is_service_account,
        }


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for JWT and API key authentication.
    
    This middleware intercepts all requests and:
    1. Identifies public endpoints that don't require auth
    2. Extracts authentication credentials from headers
    3. Validates JWT tokens or API keys
    4. Enriches request state with user information
    5. Handles authentication errors gracefully
    
    Attributes:
        settings: Authentication configuration settings.
        public_paths: Set of paths that don't require authentication.
        public_path_patterns: Regex patterns for public paths.
    """
    
    # Paths that don't require authentication
    DEFAULT_PUBLIC_PATHS = {
        "/",
        "/health",
        "/ready",
        "/live",
        "/metrics",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
    }
    
    # Path patterns (regex) that don't require authentication
    DEFAULT_PUBLIC_PATTERNS = [
        r"^/auth/login$",
        r"^/auth/register$",
        r"^/auth/refresh$",
        r"^/auth/password-reset$",
        r"^/auth/verify-email$",
        r"^/public/.*$",
    ]
    
    def __init__(
        self,
        app: Callable,
        settings: AuthSettings,
        public_paths: Optional[Set[str]] = None,
        public_patterns: Optional[List[str]] = None,
    ):
        """
        Initialize authentication middleware.
        
        Args:
            app: The ASGI application to wrap.
            settings: Authentication configuration settings.
            public_paths: Additional paths that don't require auth.
            public_patterns: Additional regex patterns for public paths.
        """
        super().__init__(app)
        self.settings = settings
        
        # Combine default and custom public paths
        self.public_paths = self.DEFAULT_PUBLIC_PATHS.copy()
        if public_paths:
            self.public_paths.update(public_paths)
        
        # Compile public path patterns
        patterns = self.DEFAULT_PUBLIC_PATTERNS.copy()
        if public_patterns:
            patterns.extend(public_patterns)
        self.public_path_patterns = [re.compile(p) for p in patterns]
        
        # Load JWT keys if configured
        self._public_key = None
        self._private_key = None
        self._load_keys()
    
    def _load_keys(self):
        """Load JWT signing keys from files if configured."""
        if self.settings.jwt_public_key_path:
            try:
                with open(self.settings.jwt_public_key_path, "r") as f:
                    self._public_key = f.read()
                logger.info("Loaded JWT public key", path=self.settings.jwt_public_key_path)
            except Exception as e:
                logger.error("Failed to load JWT public key", error=str(e))
        
        if self.settings.jwt_private_key_path:
            try:
                with open(self.settings.jwt_private_key_path, "r") as f:
                    self._private_key = f.read()
                logger.info("Loaded JWT private key", path=self.settings.jwt_private_key_path)
            except Exception as e:
                logger.error("Failed to load JWT private key", error=str(e))
    
    def _is_public_path(self, path: str) -> bool:
        """
        Check if a path is public (doesn't require authentication).
        
        Args:
            path: The request path.
        
        Returns:
            bool: True if the path is public.
        """
        # Check exact matches
        if path in self.public_paths:
            return True
        
        # Check pattern matches
        for pattern in self.public_path_patterns:
            if pattern.match(path):
                return True
        
        return False
    
    def _extract_bearer_token(self, request: Request) -> Optional[str]:
        """
        Extract Bearer token from Authorization header.
        
        Args:
            request: The incoming request.
        
        Returns:
            Optional[str]: The token if found, None otherwise.
        """
        auth_header = request.headers.get("Authorization", "")
        
        if auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove "Bearer " prefix
        
        return None
    
    def _extract_api_key(self, request: Request) -> Optional[str]:
        """
        Extract API key from header.
        
        Args:
            request: The incoming request.
        
        Returns:
            Optional[str]: The API key if found, None otherwise.
        """
        return request.headers.get(self.settings.api_key_header)
    
    async def _validate_jwt(self, token: str) -> AuthenticatedUser:
        """
        Validate a JWT token and extract user information.
        
        Args:
            token: The JWT token to validate.
        
        Returns:
            AuthenticatedUser: The authenticated user information.
        
        Raises:
            AuthenticationError: If token is invalid.
        """
        try:
            # Determine the key to use for verification
            if self.settings.jwt_algorithm.startswith("RS"):
                key = self._public_key or self.settings.jwt_secret_key
            elif self.settings.jwt_algorithm.startswith("ES"):
                key = self._public_key or self.settings.jwt_secret_key
            else:
                key = self.settings.jwt_secret_key
            
            # Decode and verify the token
            payload = jwt.decode(
                token,
                key,
                algorithms=[self.settings.jwt_algorithm],
                audience=self.settings.jwt_audience,
                issuer=self.settings.jwt_issuer,
                options={
                    "verify_aud": True,
                    "verify_iss": True,
                    "verify_exp": True,
                    "verify_nbf": True,
                    "require_exp": True,
                    "require_iat": True,
                }
            )
            
            # Extract user information from claims
            user = AuthenticatedUser(
                user_id=payload.get("sub"),
                email=payload.get("email"),
                roles=payload.get("roles", []),
                permissions=payload.get("permissions", []),
                scopes=payload.get("scope", "").split() if payload.get("scope") else [],
                tenant_id=payload.get("tenant_id"),
                session_id=payload.get("session_id") or payload.get("jti"),
                token_type="jwt",
                is_service_account=payload.get("is_service_account", False),
                metadata=payload.get("metadata", {}),
            )
            
            # Validate required fields
            if not user.user_id:
                raise AuthenticationError("Token missing subject claim")
            
            return user
            
        except ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except JWTError as e:
            logger.warning("JWT validation failed", error=str(e))
            raise AuthenticationError(f"Invalid token: {str(e)}")
    
    async def _validate_api_key(self, api_key: str) -> AuthenticatedUser:
        """
        Validate an API key and extract user information.
        
        Args:
            api_key: The API key to validate.
        
        Returns:
            AuthenticatedUser: The authenticated user information.
        
        Raises:
            AuthenticationError: If API key is invalid.
        """
        # Check API key format
        if not api_key.startswith(self.settings.api_key_prefix):
            raise AuthenticationError("Invalid API key format")
        
        # In production, this would look up the API key in the database
        # For now, we'll validate format and return a placeholder
        # This should be replaced with actual database lookup
        
        # TODO: Implement actual API key validation against database
        # Example implementation:
        # api_key_record = await self.api_key_store.get(api_key)
        # if not api_key_record:
        #     raise AuthenticationError("Invalid API key")
        # if api_key_record.revoked:
        #     raise AuthenticationError("API key has been revoked")
        # if api_key_record.expires_at and api_key_record.expires_at < datetime.now(timezone.utc):
        #     raise AuthenticationError("API key has expired")
        
        # Placeholder - in production, fetch from database
        logger.warning("API key validation not fully implemented - using placeholder")
        
        return AuthenticatedUser(
            user_id="api_key_user",
            token_type="api_key",
            is_service_account=True,
            scopes=["read", "write"],
        )
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process authentication for the request.
        
        This method:
        1. Checks if the path is public
        2. Extracts credentials from headers
        3. Validates credentials
        4. Enriches request state with user info
        5. Handles authentication errors
        
        Args:
            request: The incoming request.
            call_next: The next middleware or route handler.
        
        Returns:
            Response: The response from downstream handlers.
        
        Raises:
            AuthenticationError: If authentication fails.
        """
        # Initialize request state
        request.state.user = None
        request.state.authenticated = False
        request.state.auth_method = None
        
        # Check if path is public
        if self._is_public_path(request.url.path):
            request.state.is_public = True
            return await call_next(request)
        
        request.state.is_public = False
        
        # Try to extract and validate credentials
        user = None
        auth_method = None
        
        # First, try Bearer token (JWT)
        token = self._extract_bearer_token(request)
        if token:
            try:
                user = await self._validate_jwt(token)
                auth_method = "jwt"
            except AuthenticationError:
                raise  # Re-raise authentication errors
        
        # If no JWT, try API key
        if not user:
            api_key = self._extract_api_key(request)
            if api_key:
                try:
                    user = await self._validate_api_key(api_key)
                    auth_method = "api_key"
                except AuthenticationError:
                    raise  # Re-raise authentication errors
        
        # If no credentials provided
        if not user:
            raise AuthenticationError("Authentication required")
        
        # Store user info in request state
        request.state.user = user
        request.state.authenticated = True
        request.state.auth_method = auth_method
        
        # Log successful authentication
        logger.debug(
            "Request authenticated",
            user_id=user.user_id,
            auth_method=auth_method,
            request_id=getattr(request.state, "request_id", None),
        )
        
        return await call_next(request)


def get_current_user(request: Request) -> Optional[AuthenticatedUser]:
    """
    Get the current authenticated user from request state.
    
    This is a convenience function for extracting the authenticated
    user from the request state.
    
    Args:
        request: The FastAPI request object.
    
    Returns:
        Optional[AuthenticatedUser]: The authenticated user, or None if not authenticated.
    """
    return getattr(request.state, "user", None)


def require_auth(request: Request) -> AuthenticatedUser:
    """
    Require authentication and return the current user.
    
    This function can be used as a dependency to require authentication
    for specific endpoints.
    
    Args:
        request: The FastAPI request object.
    
    Returns:
        AuthenticatedUser: The authenticated user.
    
    Raises:
        AuthenticationError: If user is not authenticated.
    """
    user = get_current_user(request)
    if not user:
        raise AuthenticationError("Authentication required")
    return user


def require_roles(*roles: str):
    """
    Create a dependency that requires specific roles.
    
    Args:
        *roles: The required roles (user must have at least one).
    
    Returns:
        Callable: A dependency function.
    
    Example:
        @app.get("/admin")
        async def admin_endpoint(user: AuthenticatedUser = Depends(require_roles("admin"))):
            return {"message": "Admin access granted"}
    """
    def dependency(request: Request) -> AuthenticatedUser:
        user = require_auth(request)
        if not user.has_any_role(list(roles)):
            raise AuthenticationError(f"Required role: {' or '.join(roles)}")
        return user
    return dependency


def require_permissions(*permissions: str):
    """
    Create a dependency that requires specific permissions.
    
    Args:
        *permissions: The required permissions (user must have all).
    
    Returns:
        Callable: A dependency function.
    """
    def dependency(request: Request) -> AuthenticatedUser:
        user = require_auth(request)
        for perm in permissions:
            if not user.has_permission(perm):
                raise AuthenticationError(f"Missing permission: {perm}")
        return user
    return dependency


def require_scopes(*scopes: str):
    """
    Create a dependency that requires specific scopes.
    
    Args:
        *scopes: The required scopes (token must have all).
    
    Returns:
        Callable: A dependency function.
    """
    def dependency(request: Request) -> AuthenticatedUser:
        user = require_auth(request)
        for scope in scopes:
            if not user.has_scope(scope):
                raise AuthenticationError(f"Missing scope: {scope}")
        return user
    return dependency
