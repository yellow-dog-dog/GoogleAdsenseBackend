from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.models import ProxyIPs


class ProxyIpsService:
    @staticmethod
    async def add_proxy_ip(session: AsyncSession, proxy_ip: str,domain):
        """添加新的代理IP"""
        async with session.begin():
            # 检查是否已存在
            # result = await session.execute(select(ProxyIPs).filter_by(proxy_ip=proxy_ip))
            # existing_ip = result.scalar_one_or_none()
            # if existing_ip:
            #     raise ValueError(f"Proxy IP {proxy_ip} already exists")

            # 添加新IP
            new_proxy_ip = ProxyIPs(proxy_ip=proxy_ip,domain=domain)
            session.add(new_proxy_ip)
            return new_proxy_ip

    @staticmethod
    async def get_all_proxy_ips(session: AsyncSession):
        """查询所有代理IP"""
        async with session.begin():
            result = await session.execute(select(ProxyIPs))
            return result.scalars().all()

    @staticmethod
    async def get_proxy_ip_by_id(session: AsyncSession, proxy_id: int):
        """根据ID查询代理IP"""
        async with session.begin():
            result = await session.execute(select(ProxyIPs).filter_by(id=proxy_id))
            proxy_ip = result.scalar_one_or_none()
            if not proxy_ip:
                raise NoResultFound(f"No Proxy IP found with id {proxy_id}")
            return proxy_ip

    @staticmethod
    async def delete_proxy_ip(session: AsyncSession, proxy_id: int):
        """删除代理IP"""
        async with session.begin():
            result = await session.execute(select(ProxyIPs).filter_by(id=proxy_id))
            proxy_ip = result.scalar_one_or_none()
            if not proxy_ip:
                raise NoResultFound(f"No Proxy IP found with id {proxy_id}")

            await session.delete(proxy_ip)
            return proxy_ip

    @staticmethod
    async def update_proxy_ip(session: AsyncSession, proxy_id: int, new_proxy_ip: str):
        """更新代理IP"""
        async with session.begin():
            result = await session.execute(select(ProxyIPs).filter_by(id=proxy_id))
            proxy_ip = result.scalar_one_or_none()
            if not proxy_ip:
                raise NoResultFound(f"No Proxy IP found with id {proxy_id}")

            proxy_ip.proxy_ip = new_proxy_ip
            session.add(proxy_ip)
            return proxy_ip

    @staticmethod
    async def get_recent_proxy_ips(session: AsyncSession, limit: int = 10):
        """查询最近添加的代理IP"""
        async with session.begin():
            result = await session.execute(
                select(ProxyIPs).order_by(ProxyIPs.created_time.desc()).limit(limit)
            )
            return result.scalars().all()

    @staticmethod
    async def check_proxy_ip_exists(session: AsyncSession, proxy_ip: str,domain:str) -> bool:
        """检查指定的代理IP是否存在"""
        query = select(ProxyIPs).where(
            ProxyIPs.proxy_ip == proxy_ip,
            ProxyIPs.domain == domain
        )
        async with session.begin():
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None


