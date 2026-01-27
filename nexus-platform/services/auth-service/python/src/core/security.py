# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - SECURITY
# =============================================================================
# Password hashing, JWT token management, and security utilities.
# =============================================================================

"""
Security Module

Provides comprehensive security utilities including:
- Password hashing with Argon2id (OWASP recommended)
- JWT token creation and validation
- API key generation and hashing
- Secure random string generation
"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..config import settings

# =============================================================================
# PASSWORD HASHING
# =============================================================================

# Argon2id hasher (OWASP recommended)
argon2_hasher = PasswordHasher(
    time_cost=2,          # Number of iterations
    memory_cost=65536,    # Memory usage in KiB (64 MB)
    parallelism=4,        # Number of parallel threads
    hash_len=32,          # Length of the hash in bytes
    salt_len=16,          # Length of the random salt
)

# Fallback bcrypt for legacy password verification
bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash a password using Argon2id.
    
    Argon2id is the winner of the Password Hashing Competition and is
    recommended by OWASP for secure password storage.
    
    Args:
        password: The plaintext password to hash.
    
    Returns:
        str: The hashed password string.
    
    Example:
        >>> hash_password("my_secure_password")
        '$argon2id$v=19$m=65536,t=2,p=4$...'
    """
    return argon2_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Supports both Argon2id (preferred) and bcrypt (legacy) hashes.
    
    Args:
        password: The plaintext password to verify.
        hashed_password: The stored hash to verify against.
    
    Returns:
        bool: True if the password matches, False otherwise.
    """
    try:
        # Try Argon2id first
        if hashed_password.startswith("$argon2"):
            argon2_hasher.verify(hashed_password, password)
            return True
        
        # Fall back to bcrypt for legacy hashes
        if hashed_password.startswith("$2"):
            return bcrypt_context.verify(password, hashed_password)
        
        return False
        
    except VerifyMismatchError:
        return False
    except Exception:
        return False


def needs_rehash(hashed_password: str) -> bool:
    """
    Check if a password hash needs to be upgraded.
    
    Args:
        hashed_password: The stored hash to check.
    
    Returns:
        bool: True if the hash should be upgraded.
    """
    # Non-Argon2 hashes should be upgraded
    if not hashed_password.startswith("$argon2"):
        return True
    
    # Check if Argon2 parameters need updating
    try:
        return argon2_hasher.check_needs_rehash(hashed_password)
    except Exception:
        return True


# =============================================================================
# JWT TOKEN MANAGEMENT
# =============================================================================

def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: The subject (user ID) for the token.
        expires_delta: Optional custom expiration time.
        additional_claims: Additional claims to include in the token.
    
    Returns:
        str: The encoded JWT token.
    """
    now = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.jwt.access_token_expire_minutes)
    
    claims = {
        "sub": subject,
        "iat": now,
        "exp": expire,
        "nbf": now,
        "iss": settings.jwt.issuer,
        "aud": settings.jwt.audience,
        "type": "access",
    }
    
    if additional_claims:
        claims.update(additional_claims)
    
    return jwt.encode(
        claims,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )


def create_refresh_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
    session_id: Optional[str] = None,
) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        subject: The subject (user ID) for the token.
        expires_delta: Optional custom expiration time.
        session_id: Optional session ID to bind the token to.
    
    Returns:
        str: The encoded JWT refresh token.
    """
    now = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.jwt.refresh_token_expire_days)
    
    claims = {
        "sub": subject,
        "iat": now,
        "exp": expire,
        "nbf": now,
        "iss": settings.jwt.issuer,
        "aud": settings.jwt.audience,
        "type": "refresh",
        "jti": generate_token_id(),
    }
    
    if session_id:
        claims["session_id"] = session_id
    
    return jwt.encode(
        claims,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )


def decode_token(token: str, verify_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: The JWT token to decode.
        verify_type: Optional token type to verify ("access" or "refresh").
    
    Returns:
        Dict: The decoded token claims.
    
    Raises:
        JWTError: If the token is invalid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt.secret_key,
            algorithms=[settings.jwt.algorithm],
            audience=settings.jwt.audience,
            issuer=settings.jwt.issuer,
            options={
                "verify_aud": True,
                "verify_iss": True,
                "verify_exp": True,
                "verify_nbf": True,
            }
        )
        
        # Verify token type if specified
        if verify_type and payload.get("type") != verify_type:
            raise JWTError(f"Invalid token type: expected {verify_type}")
        
        return payload
        
    except JWTError:
        raise
    except Exception as e:
        raise JWTError(f"Token decode error: {str(e)}")


def create_token_pair(
    user_id: str,
    session_id: str,
    email: Optional[str] = None,
    roles: Optional[list] = None,
    permissions: Optional[list] = None,
    tenant_id: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Create an access and refresh token pair.
    
    Args:
        user_id: The user ID.
        session_id: The session ID.
        email: User's email.
        roles: User's roles.
        permissions: User's permissions.
        tenant_id: User's tenant ID.
    
    Returns:
        Tuple[str, str]: (access_token, refresh_token)
    """
    additional_claims = {
        "session_id": session_id,
    }
    
    if email:
        additional_claims["email"] = email
    if roles:
        additional_claims["roles"] = roles
    if permissions:
        additional_claims["permissions"] = permissions
    if tenant_id:
        additional_claims["tenant_id"] = tenant_id
    
    access_token = create_access_token(
        subject=user_id,
        additional_claims=additional_claims,
    )
    
    refresh_token = create_refresh_token(
        subject=user_id,
        session_id=session_id,
    )
    
    return access_token, refresh_token


# =============================================================================
# API KEY MANAGEMENT
# =============================================================================

def generate_api_key(prefix: str = "nxp_") -> Tuple[str, str]:
    """
    Generate a new API key.
    
    Returns both the full key (to show to user once) and the hash
    (to store in database).
    
    Args:
        prefix: Prefix for the API key.
    
    Returns:
        Tuple[str, str]: (full_key, key_hash)
    """
    # Generate a secure random key
    key_bytes = secrets.token_bytes(32)
    key_hex = key_bytes.hex()
    
    full_key = f"{prefix}{key_hex}"
    key_hash = hash_api_key(full_key)
    
    return full_key, key_hash


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key for storage.
    
    Uses SHA-256 for fast verification while remaining secure.
    
    Args:
        api_key: The API key to hash.
    
    Returns:
        str: The hashed API key.
    """
    return hashlib.sha256(api_key.encode()).hexdigest()


def verify_api_key(api_key: str, key_hash: str) -> bool:
    """
    Verify an API key against its hash.
    
    Args:
        api_key: The API key to verify.
        key_hash: The stored hash.
    
    Returns:
        bool: True if valid.
    """
    return secrets.compare_digest(hash_api_key(api_key), key_hash)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_token_id() -> str:
    """Generate a unique token ID (JTI)."""
    return secrets.token_urlsafe(32)


def generate_verification_token() -> str:
    """Generate a token for email/phone verification."""
    return secrets.token_urlsafe(48)


def generate_password_reset_token() -> str:
    """Generate a token for password reset."""
    return secrets.token_urlsafe(48)


def generate_otp_code(length: int = 6) -> str:
    """Generate a numeric OTP code."""
    return "".join(secrets.choice("0123456789") for _ in range(length))


def generate_backup_codes(count: int = 10) -> list:
    """Generate backup codes for MFA recovery."""
    return [
        "-".join([
            secrets.token_hex(2).upper()
            for _ in range(4)
        ])
        for _ in range(count)
    ]
