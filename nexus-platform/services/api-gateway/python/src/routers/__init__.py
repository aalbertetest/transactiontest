# =============================================================================
# NEXUS PLATFORM - API GATEWAY - ROUTERS
# =============================================================================

"""
Routers Package

This package contains API routers for the API Gateway:
- health: Health check endpoints (/health, /ready, /live)
- proxy: Dynamic proxy router for backend services
- admin: Administrative endpoints
- metrics: Prometheus metrics endpoint
"""

from . import health
from . import proxy
from . import admin

__all__ = ["health", "proxy", "admin"]
