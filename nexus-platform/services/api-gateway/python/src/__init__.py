# =============================================================================
# NEXUS PLATFORM - API GATEWAY SERVICE
# =============================================================================
# Production-grade API Gateway with routing, authentication, rate limiting,
# circuit breaking, and comprehensive observability.
# =============================================================================

"""
Nexus Platform API Gateway Service

This module provides a high-performance, production-ready API Gateway that serves
as the single entry point for all client requests to the Nexus Platform.

Features:
- Dynamic routing to backend services
- JWT and API key authentication
- Rate limiting (per-user, per-endpoint, global)
- Circuit breaker pattern for fault tolerance
- Request/response transformation
- Caching layer
- Comprehensive logging and metrics
- Distributed tracing
- Health checks
- Graceful shutdown

Architecture:
    Client -> API Gateway -> Service Discovery -> Backend Services
                  |
                  +-> Authentication
                  +-> Rate Limiting
                  +-> Circuit Breaker
                  +-> Request Validation
                  +-> Response Caching
                  +-> Metrics/Logging
"""

__version__ = "1.0.0"
__author__ = "Nexus Platform Team"

from .config import settings
from .main import create_app

__all__ = ["create_app", "settings", "__version__"]
