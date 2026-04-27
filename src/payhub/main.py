"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import select

from payhub.config import get_settings
from payhub.rate_limit import limiter
from payhub.db import SessionLocal, engine
from payhub.logging_config import configure_logging, get_logger, new_trace_id
from payhub.models import Base, User, UserRole
from payhub.routers import api_keys, health, payments, users
from payhub.auth import hash_password

configure_logging()
log = get_logger("main")


def _bootstrap_admin_if_configured() -> None:
    settings = get_settings()
    if not settings.bootstrap_admin_key:
        return
    with SessionLocal() as db:
        has_admin = db.execute(select(User).where(User.role == UserRole.admin)).first()
        if has_admin:
            return
        email = "admin@payhub.local"
        if db.execute(select(User).where(User.email == email)).first():
            return
        u = User(
            email=email,
            hashed_password=hash_password(settings.bootstrap_admin_key),
            role=UserRole.admin,
        )
        db.add(u)
        db.commit()
        log.warning("bootstrapped_admin_user", email=email)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    _bootstrap_admin_if_configured()
    yield


app = FastAPI(title="PayHub", version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def request_context(request: Request, call_next):
    rid = request.headers.get("X-Request-ID") or new_trace_id()
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=rid)
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response


@app.exception_handler(Exception)
async def unhandled(exc: Exception, request: Request):
    log.exception("unhandled_error", path=request.url.path)
    return JSONResponse(status_code=500, content={"detail": "internal_error"})


app.include_router(health.router)
app.include_router(users.router)
app.include_router(payments.router)
app.include_router(api_keys.router)


@app.get("/metrics")
def metrics_stub():
    """Placeholder for Prometheus scrape; wire real exporter in k8s."""
    return {"requests": "not_implemented_counter"}
