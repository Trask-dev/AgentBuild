from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.agent_schemas import AgentCreate, AgentResp
from services.agent_service import AgentService
from typing import List
from utils.mask import mask_api_key

router = APIRouter(prefix="/agent", tags=["智能体接口"])


# ======================
# 1. 创建智能体（REST：POST /agent）
# ======================
@router.post("", response_model=AgentResp)
def create_agent(
        req: AgentCreate,
        db: Session = Depends(get_db)
):
    agent = AgentService.create_agent(
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
    # api_key 脱敏
    agent.api_key = mask_api_key(agent.api_key)
    return agent


# ======================
# 2. 获取当前用户所有智能体（REST：GET /agent）
# ======================
@router.get("", response_model=List[AgentResp])
def get_user_agents(
        db: Session = Depends(get_db)
):
    agents = AgentService.get_user_agents(
        db=db,
        user_id=1
    )
    for agent in agents:
        agent.api_key = mask_api_key(agent.api_key)

    return agents


# ======================
# 3. 获取单个智能体（REST：GET /agent/{agent_id}）
# ======================
@router.get("/{agent_id}", response_model=AgentResp)
def get_agent(
        agent_id: int,
        db: Session = Depends(get_db)
):
    agent = AgentService.get_agent(
        db=db,
        user_id=1,
        agent_id=agent_id
    )
    # api_key 脱敏
    agent.api_key = mask_api_key(agent.api_key)
    return agent


# ======================
# 4. 更新智能体（REST：PUT /agent/{agent_id}）
# ======================
@router.put("/{agent_id}", response_model=AgentResp)
def update_agent(
        agent_id: int,
        req: AgentCreate,
        db: Session = Depends(get_db)
):
    agent = AgentService.update_agent(
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
    # api_key 脱敏
    agent.api_key = mask_api_key(agent.api_key)
    return agent


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