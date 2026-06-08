from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.chat_schemas import ChatRequest
from services.chat_service import ChatService
from fastapi.responses import StreamingResponse

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
