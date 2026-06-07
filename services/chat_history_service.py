from sqlalchemy.orm import Session
from models.chat_history_model import ChatHistory
from fastapi import HTTPException

class ChatHistoryService:

    @staticmethod
    def add_chat(
            db: Session,
            user_id: int,
            agent_id: str,
            user_msg: str,
            ai_msg: str,
            session_id: int
    ):
        """
        保存单轮对话记录
        """
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

    @staticmethod
    def get_history(
            db: Session,
            agent_id: str,
            session_id: int,
            limit: int = 10
    ):
        """
        获取当前智能体 + 会话的历史消息
        返回格式：[ {"role": "user", "content": xxx}, ... ]
        """
        chats = db.query(ChatHistory).filter(
            ChatHistory.agent_id == agent_id,
            ChatHistory.session_id == session_id
        ).order_by(ChatHistory.id.asc()).limit(limit).all()

        # 转成 Agent 需要的消息格式
        messages = []
        for chat in chats:
            messages.append({"role": "user", "content": chat.user_msg})
            messages.append({"role": "assistant", "content": chat.ai_msg})

        return messages

    @staticmethod
    def get_raw_history(
            db: Session,
            agent_id: str,
            session_id: int,
            limit: int = 20
    ):
        """
        获取原始数据库记录（用于前端展示对话列表）
        """
        return db.query(ChatHistory).filter(
            ChatHistory.agent_id == agent_id,
            ChatHistory.session_id == session_id
        ).order_by(ChatHistory.id.asc()).limit(limit).all()

    @staticmethod
    def clear_history(
            db: Session,
            agent_id: str,
            session_id: int
    ):
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
            raise HTTPException(status_code=500, detail=f"清空历史失败：{str(e)}")