#!/usr/bin/python3
"""session module to interect with my database"""

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from app.core.config import get_settings
from typing import AsyncGenerator

settings = get_settings()

engine = create_async_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True)


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        from app.db.models.user import User

        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session"""
    async_session = AsyncSession(engine, expire_on_commit=False)
    async with async_session as session:
        yield session
