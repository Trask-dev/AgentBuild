from sqlalchemy.orm import Session
from models.agent_model import Agent
from ai.agent.react_agent import ReactAgent
from fastapi import HTTPException
import json
from services.chat_history_service import ChatHistoryService
from utils.mask import mask_api_key


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
        # api_key 脱敏
        agent.api_key = mask_api_key(agent.api_key)

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
        agents = db.query(Agent).filter(Agent.user_id == user_id).all()

        # api_key 脱敏（循环处理）
        for agent in agents:
            agent.api_key = mask_api_key(agent.api_key)

        return agents

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

    # ======================
    # 流式对话
    # ======================
    @staticmethod
    def chat_stream_agent(db: Session, agent_id: int, user_id: int, session_id: int, query: str):
        # 查询Agent
        agent = db.query(Agent).filter(
            Agent.id == agent_id,
            Agent.user_id == user_id
        ).first()

        if not agent:
            yield json.dumps({"error": "智能体不存在"}, ensure_ascii=False)
            return

        try:
            # 实例化 ReactAgent
            react_agent = ReactAgent(
                model_name=agent.model_name,
                tools=agent.tools or [],
                kb_id=agent.kb_id,
                system_prompt=agent.system_prompt,
                api_key = agent.api_key,
                base_url = agent.base_url
            )

            # 获取历史记录
            chat_history = ChatHistoryService.get_history(
                db = db,
                agent_id = agent_id,
                session_id = session_id
            )

            # 流式返回
            full_answer = ""
            for chunk in react_agent.execute_stream(query, chat_history):
                full_answer += chunk
                yield chunk

            # 保存历史记录
            ChatHistoryService.add_chat(
                db=db,
                user_id=user_id,
                agent_id=agent_id,
                session_id=session_id,
                user_msg=query,
                ai_msg=full_answer.strip()
            )

        except Exception as e:
            yield json.dumps({"error": f"Agent执行异常：{str(e)}"}, ensure_ascii=False)