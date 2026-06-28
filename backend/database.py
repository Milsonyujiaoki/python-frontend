"""
Database base and session management.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine

# Create sync engine for Base and CRUD operations
sync_engine = create_engine("sqlite:///./barbershop.db", echo=False, future=True)

# Create async engine
async_engine = create_async_engine("sqlite+aiosqlite:///./barbershop.db", echo=False, future=True)

# Create session factories
SyncSessionLocal = sessionmaker(sync_engine, expire_on_commit=False)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()


def get_db() -> Session:
    """Dependency to get sync database session for CRUD operations."""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_db_session() -> AsyncSession:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
