from pydantic import BaseModel, ConfigDict


class FriendUrlDomainIn(BaseModel):
    domain: str


class FriendUrlDomainOut(BaseModel):
    id: int
    domain: str
    create_time: str

    model_config = ConfigDict(from_attributes=True)
