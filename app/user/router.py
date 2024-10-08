from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.user.crud import query_user_by_user_id
from app.user.schemas import UserBase
from app.user.service import UserService

user_router=APIRouter(prefix="/user", tags=["user"])
@user_router.get('/{user_id}',response_model=UserBase)
async def get_user(user_id,session=Depends(get_session)):
    user=await UserService.get_users(user_id=user_id,session=session)
    return user
