# =============================================================================
# NEXUS PLATFORM - API GATEWAY - SERVICES
# =============================================================================

"""
Services Package

This package contains service clients and utilities:
- service_discovery: Service discovery client
- cache: Cache client wrapper
"""

from .service_discovery import ServiceDiscovery

__all__ = ["ServiceDiscovery"]
