from core.db import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.dialects.mysql import JSON


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID，自增")
    user_id = Column(Integer, nullable=False, comment="所属用户ID，关联用户表")
    name = Column(String(100), nullable=False, comment="智能体名称")
    description = Column(String(255), nullable=True, comment="智能体描述/简介")
    avatar = Column(String(255), nullable=True, comment="智能体头像URL地址")
    system_prompt = Column(Text, nullable=True, comment="系统提示词（角色设定、指令）")
    model_name = Column(String(100), nullable=False, comment="使用的大模型")
    api_key = Column(String(255), nullable=True, comment="API密钥")
    base_url = Column(String(255), nullable=True, comment="API基础URL地址")
    kb_id = Column(Integer, nullable=True, comment="绑定的知识库ID，可为空")
    tools = Column(JSON, nullable=True, comment="启用的工具列表")
    created_time = Column(DateTime, default=func.now(), comment="创建时间")
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")