from fastapi import HTTPException
from models.agent_model import Agent
from sqlalchemy.orm import Session


class AgentService:

    # ======================
    # 创建智能体
    # ======================
    @staticmethod
    def create_agent(
            db: Session,
            user_id: int,
            name: str,
            system_prompt: str,
            model_name: str,
            api_key: str,
            base_url: str,
            description: str = None,
            avatar: str = None,
            kb_id: int = None,
            tools: list = None
    ):
        """
        创建智能体（完全匹配你的Model字段）
        """
        db_agent = Agent(
            user_id=user_id,
            name=name,
            description=description,
            avatar=avatar,
            system_prompt=system_prompt,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            kb_id=kb_id,
            tools=tools or []
        )
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return db_agent

    # ======================
    # 获取单个智能体
    # ======================
    @staticmethod
    def get_agent(
            db: Session,
            user_id: int,
            agent_id: int
    ):
        agent = db.query(Agent).filter(
            Agent.id == agent_id,
            Agent.user_id == user_id
        ).first()
        if not agent:
            raise HTTPException(status_code=404, detail="智能体不存在")

        return agent

    # ======================
    # 获取当前用户所有智能体
    # ======================
    @staticmethod
    def get_user_agents(
            db: Session,
            user_id: int
    ):
        return db.query(Agent).filter(Agent.user_id == user_id).all()

    # ======================
    # 更新智能体
    # ======================
    @staticmethod
    def update_agent(
            db: Session,
            user_id: int,
            agent_id: int,
            name: str,
            system_prompt: str,
            model_name: str,
            api_key: str,
            base_url: str,
            description: str = None,
            avatar: str = None,
            kb_id: int = None,
            tools: list = None
    ):
        agent = AgentService.get_agent(db, user_id, agent_id)

        agent.name = name
        agent.system_prompt = system_prompt
        agent.model_name = model_name
        if api_key:
            agent.api_key = api_key
        agent.base_url = base_url
        agent.description = description
        agent.avatar = avatar
        agent.kb_id = kb_id
        agent.tools = tools or []

        db.commit()
        db.refresh(agent)
        return agent

    # ======================
    # 删除智能体
    # ======================
    @staticmethod
    def delete_agent(
            db: Session,
            user_id: int,
            agent_id: int
    ):
        agent = AgentService.get_agent(db, user_id, agent_id)
        db.delete(agent)
        db.commit()
        return {"detail": "删除成功"}
