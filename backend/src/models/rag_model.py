from core.db import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, func


class RAG(Base):
    __tablename__ = "rag"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="知识库主键ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    name = Column(String(100), nullable=False, comment="知识库名称")
    description = Column(Text, nullable=True, comment="知识库描述/说明")
    avatar = Column(String(255), nullable=True, comment="知识库头像URL")

    # # RAG 向量化与切片配置
    # embedding_model = Column(String(100), comment="嵌入模型名称")
    # chunk_size = Column(Integer, default=1000, comment="文本分块大小")
    # chunk_overlap = Column(Integer, default=200, comment="分块重叠长度")

    created_time = Column(DateTime, default=func.now(), comment="创建时间")
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")