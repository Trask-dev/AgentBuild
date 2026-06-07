from sqlalchemy import Column, Integer, String, DateTime, func, PrimaryKeyConstraint, UniqueConstraint
from core.db import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    agent_id = Column(Integer, nullable=False, comment="智能体ID")
    session_id = Column(Integer, nullable=False, comment="会话序号（同一用户+agent下唯一）")
    title = Column(String(200), nullable=True, comment="会话标题")
    created_time = Column(DateTime, default=func.now(), comment="创建时间")
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

    # 唯一约束：确保同一用户在同一agent下session_id不重复
    __table_args__ = (
        UniqueConstraint('user_id', 'agent_id', 'session_id', name='uix_user_agent_session'),
    )
