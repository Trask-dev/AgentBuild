from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.chat_history_model import ChatHistory
from models.session_model import ChatSession  # 补上这个依赖


class ChatHistoryService:

    @staticmethod
    def add_chat(
        db: Session,
        user_id: int,
        agent_id: str,
        user_msg: str,
        ai_msg: str,
        session_id: int
    ) -> ChatHistory:
        """
        保存单轮对话记录
        """
        try:
            chat = ChatHistory(
                user_id=user_id,
                agent_id=agent_id,
                session_id=session_id,
                user_msg=user_msg,
                ai_msg=ai_msg
            )
            db.add(chat)
            db.commit()
            db.refresh(chat)
            return chat
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"保存对话失败：{str(e)}")

    @staticmethod
    def get_history(
        db: Session,
        agent_id: str,
        session_id: int,
        limit: int = 10
    ) -> list[dict]:
        """
        获取当前智能体 + 会话的历史消息
        返回格式：[ {"role": "user", "content": xxx}, ... ]
        """
        try:
            chats = db.query(ChatHistory).filter(
                ChatHistory.agent_id == agent_id,
                ChatHistory.session_id == session_id
            ).order_by(ChatHistory.id.asc()).limit(limit).all()

            messages = []
            for chat in chats:
                messages.append({"role": "user", "content": chat.user_msg})
                messages.append({"role": "assistant", "content": chat.ai_msg})
            return messages
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取历史失败：{str(e)}")

    @staticmethod
    def clear_history(
        db: Session,
        agent_id: str,
        session_id: int
    ) -> dict:
        """
        清空当前会话历史
        """
        try:
            db.query(ChatHistory).filter(
                ChatHistory.agent_id == agent_id,
                ChatHistory.session_id == session_id
            ).delete()
            db.commit()
            return {"detail": "清空对话历史成功"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"清空历史失败：{str(e)}")

    @staticmethod
    def get_session_history(
            db: Session,
            user_id: int,
            session_id: int,
            limit: int = 10
    ) -> list[ChatHistory]:
        """
        获取指定会话的历史记录
        """
        try:
            # 验证会话是否存在且属于当前用户
            session = db.query(ChatSession).filter(
                ChatSession.id == session_id,
                ChatSession.user_id == user_id
            ).first()

            if not session:
                raise HTTPException(status_code=404, detail="会话不存在或无权访问")

            # 直接查询历史记录（不再调用 get_raw_history）
            histories = db.query(ChatHistory).filter(
                ChatHistory.agent_id == session.agent_id,
                ChatHistory.session_id == session_id
            ).order_by(ChatHistory.id.asc()).limit(limit).all()

            return histories
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取会话历史失败：{str(e)}")