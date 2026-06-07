from sqlalchemy.orm import Session
from models.agent_model import Agent
from models.session_model import ChatSession
from ai.agent.react_agent import ReactAgent
import json
from services.chat_history_service import ChatHistoryService

class ChatService:
    # ======================
    # 流式对话
    # ======================
    @staticmethod
    def chat(db: Session, session_id: int, user_id: int, query: str):
        # 1. 查询会话
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        ).first()

        if not session:
            yield json.dumps({"error": "会话不存在"}, ensure_ascii=False)
            return

        # 2. 从会话中获取 agent_id
        agent_id = session.agent_id

        # 3. 查询Agent (验证是否存在)
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
