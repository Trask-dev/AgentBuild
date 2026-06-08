from core.db import Base
from sqlalchemy import Column, Integer, Text, TIMESTAMP, text


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, comment="用户ID")
    agent_id = Column(Integer, nullable=False, comment="智能体ID")
    session_id = Column(Integer, nullable=False, comment="会话ID")
    user_msg = Column(Text, nullable=True, comment="用户消息")
    ai_msg = Column(Text, nullable=True, comment="AI回复")
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")