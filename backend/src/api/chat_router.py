from typing import List
from core.db import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from schemas.chat_schemas import ChatRequest, ChatHistoryResp
from services.chat_history_service import ChatHistoryService
from services.chat_service import ChatService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chat", tags=["对话接口"])

# ======================
# 1. 流式对话
# ======================
@router.post("/{session_id}")
def chat_agent_stream(
        session_id: int,
        req: ChatRequest,
        db: Session = Depends(get_db)
):
    return StreamingResponse(
        ChatService.chat(
            db=db,
            user_id=req.user_id,
            session_id=session_id,
            query=req.query
        ),
        media_type="text/event-stream"
    )


# ======================
# 2. 获取会话历史对话
# ======================
@router.get("/{session_id}/history", response_model=List[ChatHistoryResp])
def get_session_history(

        session_id: int,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return ChatHistoryService.get_session_history(
        db=db,
        user_id=1,
        session_id=session_id,
        limit=limit
    )