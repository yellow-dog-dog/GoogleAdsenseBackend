from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.user.crud import add_user, query_user_by_user_id
from app.database import get_session


class UserService:
    @staticmethod
    async def get_users(user_id:str,session:AsyncSession):
        user =await query_user_by_user_id(user_id=user_id,session=session)
        return user