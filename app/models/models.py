import datetime
from uuid import uuid4

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(255), unique=True, nullable=False)
    device_name = Column(String(255), nullable=False, default='未命名设备')


class FriendUrlDomain(Base):
    __tablename__ = 'friend_url_domain'
    id = Column(String(100), primary_key=True, comment="主键", default=lambda: str(uuid4()))
    domain = Column(String(255), nullable=False, comment="域名")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")


# class Profile(Base):
#     __tablename__ = 'profiles'
#     id = Column(Integer, primary_key=True , autoincrement=True)
#     profile_id=Column(String(255), unique=True, nullable=False)
#     profile_name = Column(String(255), unique=True, nullable=False)
#     profile_context = Column(Text, nullable=True,unique=False)
#     created_time = Column(DateTime, default=datetime.datetime.now, nullable=False)
#     updated_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,nullable=False)
#
# class Task(Base):
#     __tablename__ = 'tasks'
#     id = Column(Integer, primary_key=True , autoincrement=True)
#     task_id = Column(String(255), unique=True, nullable=False)
#     task_name = Column(String(255), unique=True, nullable=False)
#     created_time = Column(DateTime, default=datetime.datetime.now, nullable=False)
#     updated_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,nullable=False)
#     profile=relationship(Profile,backref='tasks',uselist=False)
#     devices=relationship(Device,backref='tasks',uselist=True)

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    log_id = Column(String(255), unique=True, nullable=False)
    device_name = Column(String(255), unique=True, nullable=False)
    profile_name = Column(String(255), unique=True, nullable=False)
    task_name = Column(String(255), unique=True, nullable=False)
    domain = Column(String(255), unique=True, nullable=False)
    level = Column(String(255), unique=True, nullable=False)
    created_time = Column(DateTime, default=datetime.datetime.now, nullable=False)


class Stat(Base):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_name = Column(String(255), unique=True, nullable=False)


class ProxyIPs(Base):
    __tablename__ = 'proxy_ips'
    id = Column(Integer, primary_key=True, autoincrement=True)
    proxy_ip = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=False)
    created_time = Column(DateTime, default=datetime.datetime.now, nullable=False)
