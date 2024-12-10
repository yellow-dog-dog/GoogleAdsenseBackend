from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.models.models import Profile, Device


class TaskIn(BaseModel):
    task_id: str | None
    task_name: str | None
    profile_id: str | None
    device_ids: List[str] | None

class ExecuteTask(BaseModel):
    task_id: str
    task_name: str
    profile: Profile
    devices: List[Device]

class TaskOut(BaseModel):
    task_id: str | None
    task_name: str | None
    profile: Profile | None
    devices: List[Device] | None
    created_time: datetime | None
    updated_time: datetime | None
