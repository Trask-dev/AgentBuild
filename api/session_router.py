from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.session_schemas import SessionCreate, SessionResp, SessionUpdate
from services.session_service import SessionService
from typing import List

router = APIRouter(prefix="/session", tags=["会话管理"])

# 1. 创建会话
@router.post("/create", response_model=SessionResp)
def create_session(
    req: SessionCreate,
    db: Session = Depends(get_db)
):
    return SessionService.create_session(
        db=db,
        user_id=1,
        agent_id=req.agent_id,
        title=req.title
    )

# 2. 查询当前用户全部会话
@router.get("", response_model=List[SessionResp])
def get_user_sessions(
    agent_id: int = None,
    db: Session = Depends(get_db)
):
    return SessionService.get_user_sessions(
        db=db,
        user_id=1,
        agent_id=agent_id
    )

# 3. 根据id查询单条会话
@router.get("/{session_id}", response_model=SessionResp)
def get_session(
    session_id: int,
    agent_id: int = None,
    db: Session = Depends(get_db)
):
    return SessionService.get_session(
        db=db,
        session_id=session_id,
        user_id=1,
        agent_id=agent_id
    )

# 4. 修改会话标题
@router.put("/{session_id}", response_model=SessionResp)
def update_session(
    session_id: int,
    req: SessionUpdate,
    agent_id: int = None,
    db: Session = Depends(get_db)
):
    return SessionService.update_session_title(
        db=db,
        session_id=session_id,
        user_id=1,
        agent_id=agent_id,
        title=req.title
    )

# 5. 删除会话
@router.delete("/{session_id}")
def delete_session(
    session_id: int,
    agent_id: int = None,
    db: Session = Depends(get_db)
):
    return SessionService.delete_session(
        db=db,
        session_id=session_id,
        user_id=1,
        agent_id=agent_id
    )