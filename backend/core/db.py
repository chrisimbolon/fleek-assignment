# backend/core/db.py

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine 


ASYNC_DATABASE_URL = "postgresql+asyncpg://fleek_user:fleek_pass@localhost:5432/fleek_db"
SYNC_DATABASE_URL = "postgresql://fleek_user:fleek_pass@localhost:5432/fleek_db"


engine: AsyncEngine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
sync_session = sessionmaker(bind=sync_engine)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

