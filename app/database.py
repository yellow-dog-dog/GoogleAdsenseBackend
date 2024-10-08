import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings
from app.user.models import Base

async_engine=create_async_engine(url=settings.DATABASE_URL)
Session = async_sessionmaker(bind=async_engine,expire_on_commit=False,class_=AsyncSession,)

async def get_session()->AsyncSession:
    async with Session() as session:
        yield session


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# asyncio.run(init_db())
