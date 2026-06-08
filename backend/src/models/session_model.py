from core.db import Base
from sqlalchemy import Column, Integer, String, DateTime, func


class ChatSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    agent_id = Column(Integer, nullable=False, comment="智能体ID")
    title = Column(String(200), nullable=True, comment="会话标题")
    created_time = Column(DateTime, default=func.now(), comment="创建时间")
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
