import os
from typing import Generator
import redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/qevn")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Synchronous Engine & Session setup for backward compatibility
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Asynchronous Engine & Session setup for production async workers
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(
    ASYNC_DATABASE_URL, 
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10
)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

# Redis client
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class TenantSessionManager:
    """
    Session manager that enforces Row-Level Security (RLS) configurations 
    by injecting the current tenant context into the session parameters.
    """
    def __init__(self, organization_id: str):
        self.organization_id = organization_id
        self.db: Session = SessionLocal()

    def __enter__(self) -> Session:
        # Enforce Postgres session variable for RLS
        self.db.execute(text(f"SET LOCAL app.current_organization_id = '{self.organization_id}';"))
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

class AsyncTenantSessionManager:
    """
    Asynchronous session manager that enforces Row-Level Security (RLS) configurations 
    by injecting the current tenant context into the async session transaction parameters.
    """
    def __init__(self, organization_id: str):
        self.organization_id = organization_id
        self.session: AsyncSession = None

    async def __aenter__(self) -> AsyncSession:
        self.session = AsyncSessionLocal()
        # Enforce Postgres session variable for RLS
        await self.session.execute(text(f"SET LOCAL app.current_organization_id = '{self.organization_id}';"))
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

def get_redis_session() -> redis.Redis:
    return redis_client
