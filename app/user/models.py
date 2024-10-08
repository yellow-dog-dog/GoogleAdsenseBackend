from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs,DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True,nullable=False)
    user_id:Mapped[str]=mapped_column(String(80))
    username:Mapped[str]=mapped_column(String(50))
    email:Mapped[str]=mapped_column(String(50))
    password:Mapped[str]=mapped_column(String(200))
    def __repr__(self):
        return f'<User {self.user_id}, {self.username}, {self.email}, {self.password}>'
