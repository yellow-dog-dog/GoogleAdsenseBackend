import uuid

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Device
from app.schemas.device import DeviceIn


class DeviceService:
    @staticmethod
    async def add_device(session: AsyncSession, device: DeviceIn):
        device = Device(**device.model_dump())
        device.device_id = f'device_{uuid.uuid4()}'
        session.add(device)
        await session.commit()
        return device

    @staticmethod
    async def delete_device(session: AsyncSession, device_id: str):
        await session.execute(
            delete(Device).where(Device.device_id == device_id)
        )
        await session.commit()
        return device_id

    @staticmethod
    async def update_device_name(session: AsyncSession, device: DeviceIn):
        stmt = (
            update(Device).
            where(Device.device_id == device.device_id).
            values(device_name=device.device_name)
        )
        await session.execute(stmt)
        await session.commit()
        return True

    @staticmethod
    async def get_device_by_device_id(session: AsyncSession, device_id: str):
        stmt = select(Device).where(Device.device_id == device_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_device_by_device_ids(session: AsyncSession, device_ids: list):
        stmt = select(Device).where(Device.device_id.in_(device_ids))
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_all_devices(session: AsyncSession):
        stmt = select(Device)
        result = await session.execute(stmt)
        return result.scalars().all()

