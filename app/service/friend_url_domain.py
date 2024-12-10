import asyncio
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.models import FriendUrlDomain


class FriendUrlDomainService:
    @staticmethod
    async def create_friend_url(session: AsyncSession, domain: str):
        """新增友链域名"""
        new_entry = FriendUrlDomain(domain=domain)
        session.add(new_entry)
        await session.commit()
        # await session.refresh(new_entry)
        return new_entry

    @staticmethod
    async def get_friend_url_by_domain(session: AsyncSession, domain: str):
        """根据域名查询记录"""
        result = await session.execute(
            select(FriendUrlDomain).where(FriendUrlDomain.domain == domain)
        )
        return result.scalars().first()

    @staticmethod
    async def delete_friend_url_by_domain(session: AsyncSession, domain: str):
        """根据域名删除记录"""
        result = await session.execute(
            select(FriendUrlDomain).where(FriendUrlDomain.domain == domain)
        )
        record = result.scalars().first()
        if record:
            await session.delete(record)
            await session.commit()
            return 1  # 表示删除了 1 条记录
        return 0  # 表示没有找到记录

    @staticmethod
    async def count_domain_today(session: AsyncSession, domain: str):
        """统计域名在今天的出现次数"""
        today_start = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_end = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

        result = await session.execute(
            select(FriendUrlDomain)
            .where(
                FriendUrlDomain.domain == domain,
                FriendUrlDomain.create_time.between(today_start, today_end),
                )
        )
        # 将结果转换为列表并获取长度
        return len(result.scalars().all())


