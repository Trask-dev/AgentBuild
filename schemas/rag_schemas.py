from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ----------------------
# 1. 创建RAG知识库（前端 → 后端）
# ----------------------
class RAGCreate(BaseModel):
    name: str
    description: Optional[str] = None
    avatar: Optional[str] = None

# ----------------------
# 2. 返回RAG知识库信息（后端 → 前端）
# ----------------------
class RAGResp(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    avatar: Optional[str] = None
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True