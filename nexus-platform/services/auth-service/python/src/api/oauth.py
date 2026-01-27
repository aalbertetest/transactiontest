# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - OAUTH API
# =============================================================================
# OAuth2/OIDC provider integration endpoints.
# =============================================================================

"""
OAuth API Routes

Provides endpoints for:
- OAuth2 provider authentication (Google, GitHub, etc.)
- Authorization URL generation
- OAuth callback handling
- Account linking/unlinking
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from urllib.parse import urlencode
import uuid
import secrets

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import structlog

from ..config import settings
from ..core.database import get_db
from ..core.security import (
    decode_token,
    create_token_pair,
)
from ..core.redis import set_cache, get_cache, delete_cache
from ..models.user import User, UserStatus
from ..models.session import Session

logger = structlog.get_logger(__name__)
router = APIRouter()


# =============================================================================
# OAUTH PROVIDER CONFIGURATION
# =============================================================================

OAUTH_PROVIDERS = {
    "google": {
        "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v3/userinfo",
        "scopes": ["openid", "email", "profile"],
        "client_id_setting": "google_client_id",
        "client_secret_setting": "google_client_secret",
    },
    "github": {
        "authorize_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "userinfo_url": "https://api.github.com/user",
        "email_url": "https://api.github.com/user/emails",
        "scopes": ["read:user", "user:email"],
        "client_id_setting": "github_client_id",
        "client_secret_setting": "github_client_secret",
    },
}


# =============================================================================
# SCHEMAS
# =============================================================================

class OAuthProviderResponse(BaseModel):
    """OAuth provider info."""
    name: str
    enabled: bool


class OAuthAuthorizeResponse(BaseModel):
    """OAuth authorization URL response."""
    authorize_url: str
    state: str


class OAuthCallbackRequest(BaseModel):
    """OAuth callback request."""
    code: str
    state: str


class OAuthLoginResponse(BaseModel):
    """OAuth login response."""
    success: bool
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int
    user: Optional[dict] = None
    is_new_user: bool = False


class OAuthLinkResponse(BaseModel):
    """OAuth account link response."""
    success: bool
    provider: str
    linked: bool


class LinkedAccount(BaseModel):
    """Linked OAuth account info."""
    provider: str
    provider_user_id: str
    email: Optional[str] = None
    linked_at: datetime


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_provider_config(provider: str) -> dict:
    """Get OAuth provider configuration."""
    if provider not in OAUTH_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_PROVIDER", "message": f"Unknown OAuth provider: {provider}"},
        )
    
    config = OAUTH_PROVIDERS[provider]
    
    # Get client credentials from settings
    client_id = getattr(settings.oauth, config["client_id_setting"], None)
    client_secret = getattr(settings.oauth, config["client_secret_setting"], None)
    
    if not client_id or not client_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "PROVIDER_NOT_CONFIGURED", "message": f"OAuth provider not configured: {provider}"},
        )
    
    return {
        **config,
        "client_id": client_id,
        "client_secret": client_secret,
    }


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get the current authenticated user from the request."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "Authentication required"},
        )
    
    token = auth_header.split(" ")[1]
    
    try:
        payload = decode_token(token, verify_type="access")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": "Invalid or expired token"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": "Invalid token payload"},
        )
    
    result = await db.execute(
        select(User).where(User.id == uuid.UUID(user_id))
    )
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCOUNT_DISABLED", "message": "Account is disabled"},
        )
    
    return user


async def exchange_code_for_token(
    provider: str,
    code: str,
    redirect_uri: str,
) -> dict:
    """Exchange authorization code for access token."""
    config = get_provider_config(provider)
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
    }
    
    headers = {"Accept": "application/json"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            config["token_url"],
            data=data,
            headers=headers,
        )
        
        if response.status_code != 200:
            logger.error(
                "OAuth token exchange failed",
                provider=provider,
                status=response.status_code,
                response=response.text,
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "TOKEN_EXCHANGE_FAILED", "message": "Failed to exchange code for token"},
            )
        
        return response.json()


async def get_user_info(provider: str, access_token: str) -> dict:
    """Get user info from OAuth provider."""
    config = get_provider_config(provider)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            config["userinfo_url"],
            headers=headers,
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "USERINFO_FAILED", "message": "Failed to get user info"},
            )
        
        user_info = response.json()
        
        # GitHub needs separate call for email
        if provider == "github" and not user_info.get("email"):
            email_url = config.get("email_url")
            if email_url:
                email_response = await client.get(email_url, headers=headers)
                if email_response.status_code == 200:
                    emails = email_response.json()
                    # Get primary verified email
                    for email in emails:
                        if email.get("primary") and email.get("verified"):
                            user_info["email"] = email["email"]
                            break
        
        return user_info


def normalize_user_info(provider: str, user_info: dict) -> dict:
    """Normalize user info from different providers to common format."""
    if provider == "google":
        return {
            "provider_user_id": user_info.get("sub"),
            "email": user_info.get("email"),
            "email_verified": user_info.get("email_verified", False),
            "name": user_info.get("name"),
            "first_name": user_info.get("given_name"),
            "last_name": user_info.get("family_name"),
            "avatar_url": user_info.get("picture"),
        }
    elif provider == "github":
        name_parts = (user_info.get("name") or "").split(" ", 1)
        return {
            "provider_user_id": str(user_info.get("id")),
            "email": user_info.get("email"),
            "email_verified": True,  # GitHub only returns verified emails
            "name": user_info.get("name") or user_info.get("login"),
            "first_name": name_parts[0] if name_parts else None,
            "last_name": name_parts[1] if len(name_parts) > 1 else None,
            "avatar_url": user_info.get("avatar_url"),
            "username": user_info.get("login"),
        }
    
    return user_info


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get("/providers")
async def list_oauth_providers() -> list:
    """
    List available OAuth providers.
    """
    providers = []
    
    for name in OAUTH_PROVIDERS.keys():
        client_id_setting = OAUTH_PROVIDERS[name]["client_id_setting"]
        client_id = getattr(settings.oauth, client_id_setting, None)
        
        providers.append(OAuthProviderResponse(
            name=name,
            enabled=bool(client_id),
        ))
    
    return providers


@router.get("/{provider}/authorize", response_model=OAuthAuthorizeResponse)
async def get_authorize_url(
    provider: str,
    redirect_uri: Optional[str] = None,
) -> OAuthAuthorizeResponse:
    """
    Get OAuth authorization URL for a provider.
    """
    config = get_provider_config(provider)
    
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    
    # Store state in cache
    await set_cache(
        f"oauth_state:{state}",
        {
            "provider": provider,
            "redirect_uri": redirect_uri or settings.oauth.redirect_url,
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
        ttl=600,  # 10 minutes
    )
    
    # Build authorization URL
    params = {
        "client_id": config["client_id"],
        "redirect_uri": redirect_uri or settings.oauth.redirect_url,
        "response_type": "code",
        "scope": " ".join(config["scopes"]),
        "state": state,
    }
    
    # Provider-specific params
    if provider == "google":
        params["access_type"] = "offline"
        params["prompt"] = "select_account"
    
    authorize_url = f"{config['authorize_url']}?{urlencode(params)}"
    
    return OAuthAuthorizeResponse(
        authorize_url=authorize_url,
        state=state,
    )


@router.post("/{provider}/callback", response_model=OAuthLoginResponse)
async def oauth_callback(
    provider: str,
    request: OAuthCallbackRequest,
    http_request: Request,
    db: AsyncSession = Depends(get_db),
) -> OAuthLoginResponse:
    """
    Handle OAuth callback and authenticate user.
    """
    # Verify state
    state_data = await get_cache(f"oauth_state:{request.state}")
    
    if not state_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_STATE", "message": "Invalid or expired state"},
        )
    
    if state_data.get("provider") != provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "STATE_MISMATCH", "message": "State provider mismatch"},
        )
    
    # Clear state
    await delete_cache(f"oauth_state:{request.state}")
    
    redirect_uri = state_data.get("redirect_uri", settings.oauth.redirect_url)
    
    # Exchange code for token
    token_data = await exchange_code_for_token(provider, request.code, redirect_uri)
    access_token = token_data.get("access_token")
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "NO_ACCESS_TOKEN", "message": "No access token received"},
        )
    
    # Get user info
    provider_user_info = await get_user_info(provider, access_token)
    user_info = normalize_user_info(provider, provider_user_info)
    
    if not user_info.get("email"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "NO_EMAIL", "message": "Email not provided by OAuth provider"},
        )
    
    email = user_info["email"].lower()
    provider_user_id = user_info["provider_user_id"]
    
    # Check if user exists
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()
    
    is_new_user = False
    
    if not user:
        # Create new user
        is_new_user = True
        user = User(
            email=email,
            email_verified=user_info.get("email_verified", False),
            password_hash="",  # OAuth users don't have passwords
            display_name=user_info.get("name"),
            first_name=user_info.get("first_name"),
            last_name=user_info.get("last_name"),
            avatar_url=user_info.get("avatar_url"),
            username=user_info.get("username"),
            status=UserStatus.ACTIVE,
            roles=["user"],
            permissions=[],
            metadata={
                "oauth_providers": {
                    provider: {
                        "provider_user_id": provider_user_id,
                        "linked_at": datetime.now(timezone.utc).isoformat(),
                    }
                }
            },
        )
        
        db.add(user)
        await db.flush()
        
        logger.info(
            "New user created via OAuth",
            user_id=str(user.id),
            email=email,
            provider=provider,
        )
    else:
        # Update OAuth provider info
        oauth_providers = user.metadata.get("oauth_providers", {})
        if provider not in oauth_providers:
            oauth_providers[provider] = {
                "provider_user_id": provider_user_id,
                "linked_at": datetime.now(timezone.utc).isoformat(),
            }
            user.metadata["oauth_providers"] = oauth_providers
        
        # Verify email if it wasn't before
        if user_info.get("email_verified") and not user.email_verified:
            user.email_verified = True
    
    # Check user status
    if not user.is_active():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCOUNT_DISABLED", "message": "Account is disabled"},
        )
    
    # Create session
    client_ip = http_request.client.host if http_request.client else "unknown"
    session_id = str(uuid.uuid4())
    
    session = Session(
        user_id=user.id,
        refresh_token_jti=session_id,
        ip_address=client_ip,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.jwt.refresh_token_expire_days),
        metadata={"oauth_provider": provider},
    )
    db.add(session)
    
    # Update last login
    user.last_login_at = datetime.now(timezone.utc)
    
    # Generate tokens
    access_token, refresh_token = create_token_pair(
        user_id=str(user.id),
        session_id=session_id,
        email=user.email,
        roles=user.roles,
        permissions=user.permissions,
        tenant_id=str(user.tenant_id) if user.tenant_id else None,
    )
    
    logger.info(
        "OAuth login successful",
        user_id=str(user.id),
        email=email,
        provider=provider,
        is_new_user=is_new_user,
    )
    
    return OAuthLoginResponse(
        success=True,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=settings.jwt.access_token_expire_minutes * 60,
        user={
            "id": str(user.id),
            "email": user.email,
            "display_name": user.display_name,
            "roles": user.roles,
            "mfa_enabled": user.mfa_enabled,
        },
        is_new_user=is_new_user,
    )


@router.get("/{provider}/redirect")
async def oauth_redirect(
    provider: str,
    code: str,
    state: str,
):
    """
    OAuth redirect endpoint for browser-based flows.
    
    Redirects to the frontend with the authorization code.
    """
    # Verify state exists
    state_data = await get_cache(f"oauth_state:{state}")
    
    if not state_data:
        return RedirectResponse(
            url=f"{settings.oauth.redirect_url}?error=invalid_state"
        )
    
    # Redirect to frontend callback URL with code and state
    redirect_url = state_data.get("redirect_uri", settings.oauth.redirect_url)
    return RedirectResponse(
        url=f"{redirect_url}?code={code}&state={state}&provider={provider}"
    )


# =============================================================================
# ACCOUNT LINKING
# =============================================================================

@router.post("/{provider}/link", response_model=OAuthLinkResponse)
async def link_oauth_account(
    provider: str,
    code: str,
    state: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> OAuthLinkResponse:
    """
    Link an OAuth account to the current user.
    """
    # Verify state
    state_data = await get_cache(f"oauth_state:{state}")
    
    if not state_data or state_data.get("provider") != provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_STATE", "message": "Invalid or expired state"},
        )
    
    await delete_cache(f"oauth_state:{state}")
    
    redirect_uri = state_data.get("redirect_uri", settings.oauth.redirect_url)
    
    # Exchange code for token
    token_data = await exchange_code_for_token(provider, code, redirect_uri)
    access_token = token_data.get("access_token")
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "NO_ACCESS_TOKEN", "message": "No access token received"},
        )
    
    # Get user info
    provider_user_info = await get_user_info(provider, access_token)
    user_info = normalize_user_info(provider, provider_user_info)
    provider_user_id = user_info["provider_user_id"]
    
    # Check if this OAuth account is already linked to another user
    result = await db.execute(
        select(User).where(User.id != user.id)
    )
    for other_user in result.scalars().all():
        oauth_providers = other_user.metadata.get("oauth_providers", {})
        if provider in oauth_providers:
            if oauth_providers[provider].get("provider_user_id") == provider_user_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={"code": "ALREADY_LINKED", "message": "OAuth account is linked to another user"},
                )
    
    # Link account
    oauth_providers = user.metadata.get("oauth_providers", {})
    oauth_providers[provider] = {
        "provider_user_id": provider_user_id,
        "email": user_info.get("email"),
        "linked_at": datetime.now(timezone.utc).isoformat(),
    }
    user.metadata["oauth_providers"] = oauth_providers
    user.updated_at = datetime.now(timezone.utc)
    
    logger.info(
        "OAuth account linked",
        user_id=str(user.id),
        provider=provider,
    )
    
    return OAuthLinkResponse(
        success=True,
        provider=provider,
        linked=True,
    )


@router.delete("/{provider}/unlink")
async def unlink_oauth_account(
    provider: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Unlink an OAuth account from the current user.
    """
    oauth_providers = user.metadata.get("oauth_providers", {})
    
    if provider not in oauth_providers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "NOT_LINKED", "message": "OAuth account not linked"},
        )
    
    # Ensure user has a password or another OAuth provider
    if not user.password_hash and len(oauth_providers) <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "CANNOT_UNLINK",
                "message": "Cannot unlink last OAuth provider without password set",
            },
        )
    
    del oauth_providers[provider]
    user.metadata["oauth_providers"] = oauth_providers
    user.updated_at = datetime.now(timezone.utc)
    
    logger.info(
        "OAuth account unlinked",
        user_id=str(user.id),
        provider=provider,
    )
    
    return {"success": True, "message": f"Unlinked {provider} account"}


@router.get("/linked-accounts")
async def get_linked_accounts(
    user: User = Depends(get_current_user),
) -> list:
    """
    Get all linked OAuth accounts for the current user.
    """
    oauth_providers = user.metadata.get("oauth_providers", {})
    
    accounts = []
    for provider, data in oauth_providers.items():
        accounts.append(LinkedAccount(
            provider=provider,
            provider_user_id=data.get("provider_user_id", ""),
            email=data.get("email"),
            linked_at=datetime.fromisoformat(data.get("linked_at", datetime.now(timezone.utc).isoformat())),
        ))
    
    return accounts
