import asyncio

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import  AsyncSession

from app.database import get_session
from app.user.models import User


async def add_user(user,session:AsyncSession=Depends(get_session)):
    session.add(user)
    await session.commit()

async def delete_user(user,session:AsyncSession=Depends(get_session)):
    await session.delete(user)
    await session.commit()

async def update_user(user,session:AsyncSession=Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user.id))
    existing_user=result.scalar_one_or_none()
    if not existing_user:
        raise ValueError(f"User with id {user.id} not found")
    for attr,value in user.__dict__.items():
        if attr != 'id' and value is not None:
            setattr(existing_user,attr,value)
    await session.commit()


async def query_user_by_user_id(user_id:str,session:AsyncSession):
    result=await session.execute(select(User).where(User.user_id == user_id))
    user=result.scalar()
    return user
