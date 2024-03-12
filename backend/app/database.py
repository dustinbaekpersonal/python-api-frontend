"""Define database connection."""
from collections.abc import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings as global_settings

# Get database url from config file
engine = create_async_engine(
    global_settings.asyncpg_url.unicode_string(),
    future=True,
    echo=True,
)
logger.info("PostgreSQL engine started using asyncpg driver.")

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)

# Dependency
async def get_db() -> AsyncGenerator:
    """Yields a database object."""
    async with AsyncSessionFactory() as session:
        logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        yield session
