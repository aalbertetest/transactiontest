# =============================================================================
# NEXUS PLATFORM - API GATEWAY - TRACING MIDDLEWARE
# =============================================================================
# OpenTelemetry distributed tracing for request tracking.
# =============================================================================

"""
Tracing Middleware

This middleware implements distributed tracing using OpenTelemetry,
enabling end-to-end request tracking across all services.

Features:
- Automatic span creation for each request
- Context propagation (W3C Trace Context)
- Integration with Jaeger/Zipkin
- Custom attributes and events
- Error recording
- Sampling configuration
"""

from typing import Callable, Dict, Optional

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ..config import TracingSettings

logger = structlog.get_logger(__name__)

# Try to import OpenTelemetry - graceful degradation if not available
try:
    from opentelemetry import trace
    from opentelemetry.trace import SpanKind, Status, StatusCode
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
    
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    logger.warning("OpenTelemetry not available - tracing disabled")


class TracingMiddleware(BaseHTTPMiddleware):
    """
    Distributed tracing middleware using OpenTelemetry.
    
    This middleware creates spans for each incoming request and
    propagates trace context to downstream services.
    
    Attributes:
        settings: Tracing configuration.
        tracer: OpenTelemetry tracer instance.
        propagator: Context propagator for distributed tracing.
    """
    
    # Headers to extract trace context from
    TRACE_HEADERS = [
        "traceparent",
        "tracestate",
        "x-b3-traceid",
        "x-b3-spanid",
        "x-b3-sampled",
    ]
    
    def __init__(
        self,
        app: Callable,
        settings: TracingSettings,
    ):
        """
        Initialize tracing middleware.
        
        Args:
            app: The ASGI application to wrap.
            settings: Tracing configuration.
        """
        super().__init__(app)
        self.settings = settings
        self.tracer = None
        self.propagator = None
        
        if OPENTELEMETRY_AVAILABLE and settings.enabled:
            self._setup_tracing()
    
    def _setup_tracing(self) -> None:
        """Configure OpenTelemetry tracing."""
        # Create resource with service info
        resource = Resource.create({
            SERVICE_NAME: self.settings.service_name,
            SERVICE_VERSION: "1.0.0",
            "deployment.environment": "production",
        })
        
        # Create tracer provider
        provider = TracerProvider(resource=resource)
        
        # Configure Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name=self.settings.jaeger_host,
            agent_port=self.settings.jaeger_port,
        )
        
        # Add batch processor for efficient export
        provider.add_span_processor(
            BatchSpanProcessor(jaeger_exporter)
        )
        
        # Set as global provider
        trace.set_tracer_provider(provider)
        
        # Get tracer
        self.tracer = trace.get_tracer(
            self.settings.service_name,
            "1.0.0",
        )
        
        # Configure propagator
        self.propagator = TraceContextTextMapPropagator()
        
        # Instrument HTTPX for outgoing requests
        HTTPXClientInstrumentor().instrument()
        
        logger.info(
            "OpenTelemetry tracing configured",
            service=self.settings.service_name,
            jaeger_host=self.settings.jaeger_host,
            jaeger_port=self.settings.jaeger_port,
        )
    
    def _extract_context(self, request: Request) -> Optional[object]:
        """
        Extract trace context from incoming request headers.
        
        Args:
            request: The incoming request.
        
        Returns:
            Trace context if found, None otherwise.
        """
        if not self.propagator:
            return None
        
        # Create carrier from headers
        carrier = {}
        for header in self.TRACE_HEADERS:
            value = request.headers.get(header)
            if value:
                carrier[header] = value
        
        # Extract context
        return self.propagator.extract(carrier)
    
    def _get_span_name(self, request: Request) -> str:
        """
        Generate span name from request.
        
        Args:
            request: The incoming request.
        
        Returns:
            str: Span name.
        """
        return f"{request.method} {request.url.path}"
    
    def _get_span_attributes(self, request: Request) -> Dict:
        """
        Get span attributes from request.
        
        Args:
            request: The incoming request.
        
        Returns:
            Dict: Span attributes.
        """
        attributes = {
            "http.method": request.method,
            "http.url": str(request.url),
            "http.scheme": request.url.scheme,
            "http.host": request.url.netloc,
            "http.target": request.url.path,
            "http.user_agent": request.headers.get("User-Agent", ""),
            "http.request_content_length": request.headers.get("Content-Length", 0),
        }
        
        # Add request ID if available
        request_id = getattr(request.state, "request_id", None)
        if request_id:
            attributes["request.id"] = request_id
        
        # Add correlation ID if available
        correlation_id = getattr(request.state, "correlation_id", None)
        if correlation_id:
            attributes["correlation.id"] = correlation_id
        
        # Add client IP
        client_ip = request.headers.get("X-Forwarded-For")
        if client_ip:
            attributes["http.client_ip"] = client_ip.split(",")[0].strip()
        elif request.client:
            attributes["http.client_ip"] = request.client.host
        
        return attributes
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Create tracing span for the request.
        
        Args:
            request: The incoming request.
            call_next: The next middleware or route handler.
        
        Returns:
            Response: The response.
        """
        # Skip if tracing not configured
        if not self.tracer or not self.settings.enabled:
            return await call_next(request)
        
        # Skip tracing for health endpoints
        if request.url.path in ("/health", "/ready", "/live", "/metrics"):
            return await call_next(request)
        
        # Extract trace context from incoming request
        context = self._extract_context(request)
        
        # Create span
        with self.tracer.start_as_current_span(
            self._get_span_name(request),
            context=context,
            kind=SpanKind.SERVER,
            attributes=self._get_span_attributes(request),
        ) as span:
            # Store span in request state for access by handlers
            request.state.span = span
            
            # Store trace ID for logging correlation
            if span.get_span_context().is_valid:
                request.state.trace_id = format(span.get_span_context().trace_id, "032x")
                request.state.span_id = format(span.get_span_context().span_id, "016x")
            
            try:
                response = await call_next(request)
                
                # Record response attributes
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute(
                    "http.response_content_length",
                    response.headers.get("Content-Length", 0),
                )
                
                # Set span status based on response code
                if response.status_code >= 500:
                    span.set_status(Status(StatusCode.ERROR, "Server Error"))
                elif response.status_code >= 400:
                    span.set_status(Status(StatusCode.ERROR, "Client Error"))
                else:
                    span.set_status(Status(StatusCode.OK))
                
                return response
                
            except Exception as e:
                # Record exception
                if self.settings.record_exception:
                    span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise


def get_current_span() -> Optional[object]:
    """
    Get the current active span.
    
    Returns:
        The current span if tracing is enabled, None otherwise.
    """
    if not OPENTELEMETRY_AVAILABLE:
        return None
    
    return trace.get_current_span()


def add_span_attribute(key: str, value) -> None:
    """
    Add an attribute to the current span.
    
    Args:
        key: Attribute key.
        value: Attribute value.
    """
    span = get_current_span()
    if span:
        span.set_attribute(key, value)


def add_span_event(name: str, attributes: Dict = None) -> None:
    """
    Add an event to the current span.
    
    Args:
        name: Event name.
        attributes: Event attributes.
    """
    span = get_current_span()
    if span:
        span.add_event(name, attributes=attributes or {})


def create_child_span(name: str, attributes: Dict = None):
    """
    Create a child span for the current span.
    
    This is a context manager for creating nested spans.
    
    Args:
        name: Span name.
        attributes: Span attributes.
    
    Returns:
        Context manager that yields the new span.
    
    Example:
        with create_child_span("database_query") as span:
            span.set_attribute("db.statement", query)
            result = await db.execute(query)
    """
    if not OPENTELEMETRY_AVAILABLE:
        from contextlib import nullcontext
        return nullcontext()
    
    tracer = trace.get_tracer(__name__)
    return tracer.start_as_current_span(
        name,
        attributes=attributes or {},
    )
