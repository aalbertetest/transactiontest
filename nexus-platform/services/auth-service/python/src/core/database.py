# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - DATABASE
# =============================================================================
# Database connection and session management.
# =============================================================================

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from ..config import settings

# Create async engine
engine = create_async_engine(
    settings.database.url,
    pool_size=settings.database.pool_size,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    echo=settings.debug,
)

# Create session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


async def init_db() -> None:
    """Initialize database (create tables if not exist)."""
    async with engine.begin() as conn:
        # Import models to register them
        from ..models import user, session, api_key, mfa
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session dependency.
    
    Usage:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
