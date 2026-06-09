from typing import List

from core.db import get_db
from fastapi import APIRouter, Depends
from schemas.agent_schemas import AgentCreate, AgentResp
from services.agent_service import AgentService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/agent", tags=["智能体接口"])


# ======================
# 1. 创建智能体（REST：POST /agent）
# ======================
@router.post("", response_model=AgentResp)
def create_agent(
        req: AgentCreate,
        db: Session = Depends(get_db)
):
    return AgentService.create_agent(
        db=db,
        user_id=1,
        name=req.name,
        system_prompt=req.system_prompt,
        model_name=req.model_name,
        api_key=req.api_key,
        base_url=req.base_url,
        description=req.description,
        avatar=req.avatar,
        kb_id=req.kb_id,
        tools=req.tools
    )


# ======================
# 2. 获取当前用户所有智能体（REST：GET /agent）
# ======================
@router.get("", response_model=List[AgentResp])
def get_user_agents(
        db: Session = Depends(get_db)
):
    return AgentService.get_user_agents(
        db=db,
        user_id=1
    )


# ======================
# 3. 获取单个智能体（REST：GET /agent/{agent_id}）
# ======================
@router.get("/{agent_id}", response_model=AgentResp)
def get_agent(
        agent_id: int,
        db: Session = Depends(get_db)
):
    return AgentService.get_agent(
        db=db,
        user_id=1,
        agent_id=agent_id
    )


# ======================
# 4. 更新智能体（REST：PUT /agent/{agent_id}）
# ======================
@router.put("/{agent_id}", response_model=AgentResp)
def update_agent(
        agent_id: int,
        req: AgentCreate,
        db: Session = Depends(get_db)
):
    return AgentService.update_agent(
        db=db,
        user_id=1,
        agent_id=agent_id,
        name=req.name,
        system_prompt=req.system_prompt,
        model_name=req.model_name,
        api_key=req.api_key,
        base_url=req.base_url,
        description=req.description,
        avatar=req.avatar,
        kb_id=req.kb_id,
        tools=req.tools
    )


# ======================
# 5. 删除智能体（REST：DELETE /agent/{agent_id}）
# ======================
@router.delete("/{agent_id}")
def delete_agent(
        agent_id: int,
        db: Session = Depends(get_db)
):
    return AgentService.delete_agent(
        db=db,
        user_id=1,
        agent_id=agent_id
    )