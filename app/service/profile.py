import uuid

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.profile import ProfileIn
from app.models.models import Profile


class ProfileService:
    @staticmethod
    async def add_profile(session: AsyncSession, profile_in: ProfileIn):
        profile = Profile(**profile_in.model_dump())
        profile.profile_id = f'profile_{uuid.uuid4()}'
        session.add(profile)
        await session.commit()
        return True

    @staticmethod
    async def delete_profile_by_profile_id(session: AsyncSession, profile_id: str):
        stmt = delete(Profile).where(Profile.profile_id == profile_id)
        await session.execute(stmt)
        await session.commit()
        return True

    @staticmethod
    async def update_profile_by_profile_id(session: AsyncSession, profile_in: ProfileIn):
        result=await session.execute(select(Profile).where(Profile.profile_id == profile_in.profile_id))
        profile:Profile=result.scalar_one_or_none()
        if profile_in.profile_name:
            profile.profile_name = profile_in.profile_name
        if profile_in.profile_context:
            profile.profile_context = profile_in.profile_context
        await session.commit()
        return True

    @staticmethod
    async def get_profile_by_profile_id(session: AsyncSession, profile_id: str):
        stmt = select(Profile).where(Profile.profile_id == profile_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()  # 假设只返回一个结果

    @staticmethod
    async def get_all_profiles(session: AsyncSession):
        stmt = select(Profile).order_by(Profile.profile_id)
        result = await session.execute(stmt)
        return result.scalars().all()
