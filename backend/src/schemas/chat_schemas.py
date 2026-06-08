from datetime import datetime
from pydantic import BaseModel

# ----------------------
# 1. 对话请求（前端 → 后端）
# ----------------------
class ChatRequest(BaseModel):
    user_id: int
    query: str

# ----------------------
# 2. 对话历史响应（后端 → 前端）
# ----------------------
class ChatHistoryResp(BaseModel):
    id: int
    user_id: int
    agent_id: int
    session_id: int
    user_msg: str
    ai_msg: str
    create_time: datetime

    class Config:
        from_attributes = True