import uuid
from typing import Dict
from typing import List

from fastapi import WebSocket
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Task
from app.schemas.task import TaskIn
from app.schemas.ws import WebSocketMessage
from app.service.device import DeviceService
from app.service.profile import ProfileService


class TaskService:
    @staticmethod
    async def add_task(session: AsyncSession, task_in: TaskIn)->bool:
        task = Task(**task_in.model_dump())
        task.task_id = f'task_{uuid.uuid4()}'

        task.profile = await ProfileService.get_profile_by_profile_id(session, profile_id=task_in.profile_id)
        task.devices = await DeviceService.get_device_by_device_ids(session, device_ids=task_in.device_ids)

        session.add(task)
        await session.commit()
        return True

    @staticmethod
    async def delete_task(session: AsyncSession, task_id)->bool:
        stmt = delete(Task).where(Task.task_id == task_id)
        await session.execute(stmt)
        await session.commit()
        return True

    @staticmethod
    async def update_task(session: AsyncSession, task_in: TaskIn)->bool:
        result=await session.execute(select(Task).where(Task.task_id==task_in.task_id))
        task:Task=result.scalar_one_or_none()
        if task_in.task_name:
            task.task_name = task_in.task_name
        if task_in.profile_id:
            task.profile=await ProfileService.get_profile_by_profile_id(session, profile_id=task_in.profile_id)
        if task_in.device_ids:
            task.devices=await DeviceService.get_device_by_device_ids(session, device_ids=task_in.device_ids)
        await session.commit()
        return True

    @staticmethod
    async def get_task_by_task_id(session: AsyncSession, task_id: str)-> Task:
        stmt = select(Task).where(Task.task_id == task_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all_tasks(session: AsyncSession)->List[Task]:
        stmt = select(Task)
        result = await session.execute(stmt)
        return list(result.scalars().all())



    @staticmethod
    async def execute_task(online_device: Dict['str', WebSocket], payload):
        for device_id, ws in online_device.items():
            message = WebSocketMessage(
                type='command',
                payload=payload,
                sender_id='Server',
                command='start'
            )
            await ws.send_json(**message.model_dump())
        return True

    @staticmethod
    async def stop_task(online_device: Dict['str', WebSocket], payload):
        for device_id, ws in online_device.items():
            message = WebSocketMessage(
                type='command',
                payload=payload,
                sender_id='Server',
                command='stop'
            )
            await ws.send_json(**message.model_dump())
        return True

