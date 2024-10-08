from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
class UserCreate(UserBase):
    password:str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str


