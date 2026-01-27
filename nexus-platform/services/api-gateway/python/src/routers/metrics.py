# =============================================================================
# NEXUS PLATFORM - API GATEWAY - METRICS ROUTER
# =============================================================================
# Prometheus metrics endpoint.
# =============================================================================

"""
Metrics Router

This module provides the Prometheus metrics endpoint for scraping.
"""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

router = APIRouter()


@router.get(
    "/metrics",
    response_class=PlainTextResponse,
    summary="Prometheus Metrics",
    description="Expose Prometheus metrics for scraping.",
    include_in_schema=False,
)
async def metrics():
    """
    Prometheus metrics endpoint.
    
    Returns metrics in Prometheus exposition format.
    
    Returns:
        PlainTextResponse: Metrics in Prometheus format.
    """
    return PlainTextResponse(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
