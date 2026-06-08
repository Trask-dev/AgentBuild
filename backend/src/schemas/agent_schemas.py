from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


# ----------------------
# 1. 创建智能体（前端 → 后端）
# ----------------------
class AgentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    avatar: Optional[str] = None
    system_prompt: str
    model_name: str
    api_key: str
    base_url: str
    kb_id: Optional[int] = None
    tools: Optional[List[str]] = None

# ----------------------
# 2. 返回智能体信息（后端 → 前端）
# ----------------------
class AgentResp(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    avatar: Optional[str] = None
    system_prompt: str
    model_name: str
    api_key: str
    base_url: str
    kb_id: Optional[int] = None
    tools: Optional[List[str]] = None
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True