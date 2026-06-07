from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# ----------------------
# 1. 创建会话（前端 → 后端）
# ----------------------
class SessionCreate(BaseModel):
    user_id: int
    agent_id: int
    title: Optional[str] = None

# ----------------------
# 2. 更新会话（前端 → 后端）
# ----------------------
class SessionUpdate(BaseModel):
    user_id: int
    agent_id: int
    title: str

# ----------------------
# 3. 返回会话信息（后端 → 前端）
# ----------------------
class SessionResp(BaseModel):
    id: int
    user_id: int
    agent_id: int
    session_id: int
    title: Optional[str] = None
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True

# ----------------------
# 4. 返回会话列表（后端 → 前端）
# ----------------------
class SessionListResp(BaseModel):
    sessions: List[SessionResp]
    total: int