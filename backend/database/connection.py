"""AgentForge AI – Database Connection & Session Management"""

import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from backend.core.config import settings
from backend.database.models import Base

logger = logging.getLogger(__name__)

engine: AsyncEngine | None = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


async def init_db():
    """Initialize the database engine and create all tables."""
    global engine, AsyncSessionLocal

    db_url = settings.effective_database_url
    # Convert sync sqlite URL to async
    if db_url.startswith("sqlite:///"):
        db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    elif db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

    engine = create_async_engine(
        db_url,
        echo=settings.debug,
        pool_pre_ping=True,
    )
    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info(f"Database initialized: {db_url}")


async def close_db():
    """Cleanup database connections."""
    if engine:
        await engine.dispose()


@asynccontextmanager
async def get_session():
    """Context manager for database sessions."""
    if AsyncSessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_db():
    """FastAPI dependency for database sessions."""
    async with get_session() as session:
        yield session
