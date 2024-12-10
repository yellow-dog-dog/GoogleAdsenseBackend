from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings
async_engine=create_async_engine(url=settings.DATABASE_URL)
AsyncSessionFactory = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

