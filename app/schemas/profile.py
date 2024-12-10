from datetime import datetime

from pydantic import BaseModel


class ProfileIn(BaseModel):
    profile_id: str | None
    profile_name: str | None
    profile_context: str


class ProfileOut(BaseModel):
    profile_id: str | None
    profile_name: str
    profile_context: str
    created_time: datetime | None
    updated_time: datetime | None
