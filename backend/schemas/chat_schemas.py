from pydantic import BaseModel

# ----------------------
# 1. 对话请求（前端 → 后端）
# ----------------------
class ChatRequest(BaseModel):
    user_id: int
    query: str