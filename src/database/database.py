from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base

from src.config.config import settings

engine = create_async_engine(url=settings.DATABASE_URL, echo=True)

# Define a declarative base
Base = declarative_base()


# Define your User model

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Create all tables
# Base.metadata.create_all(bind=engine)


async def get_db():
    await create_tables()

    async with AsyncSession(engine) as session:
        yield session
