from pydantic import BaseModel, ConfigDict


class DeviceIn(BaseModel):
    device_id: str | None
    device_name: str


class DeviceOut(BaseModel):
    id: int
    device_id: str
    device_name: str

    model_config = ConfigDict(from_attributes=True)
