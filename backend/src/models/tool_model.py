from core.db import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, func


class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(50), nullable=False, unique=True, comment="工具名称")
    description = Column(Text, nullable=True, comment="工具描述")
    created_time = Column(DateTime, default=func.now(), comment="创建时间")
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
