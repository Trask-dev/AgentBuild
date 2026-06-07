from sqlalchemy.orm import Session
from models.session_model import Session as SessionModel
from models.chat_history_model import ChatHistory
from fastapi import HTTPException
from datetime import datetime


class SessionService:

    @staticmethod
    def create_session(
            db: Session,
            user_id: int,
            agent_id: int,
            title: str = None
    ):
        """
        创建新会话 - 自动生成自增会话序号 session_id
        """
        if not title:
            title = f"会话 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # 获取当前用户在该 agent 下的最大 session_id
        max_session = db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.agent_id == agent_id
        ).order_by(SessionModel.session_id.desc()).first()

        next_session_id = (max_session.session_id + 1) if max_session else 1

        session = SessionModel(
            user_id=user_id,
            agent_id=agent_id,
            session_id=next_session_id,
            title=title
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_session(
            db: Session,
            session_id: int,
            user_id: int,
            agent_id: int
    ):
        """
        获取单个会话信息
        """
        session = db.query(SessionModel).filter(
            SessionModel.id == session_id,
            SessionModel.user_id == user_id,
            SessionModel.agent_id == agent_id
        ).first()

        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")

        return session

    @staticmethod
    def get_user_sessions(
            db: Session,
            user_id: int,
            agent_id: int = None
    ):
        """
        获取当前用户所有会话（可按 agent_id 筛选）
        """
        query = db.query(SessionModel).filter(SessionModel.user_id == user_id)

        if agent_id:
            query = query.filter(SessionModel.agent_id == agent_id)

        return query.order_by(SessionModel.updated_time.desc()).all()

    @staticmethod
    def update_session_title(
            db: Session,
            session_id: int,
            user_id: int,
            agent_id: int,
            title: str
    ):
        """
        更新会话标题
        """
        session = SessionService.get_session(db, session_id, user_id, agent_id)

        session.title = title
        session.updated_time = datetime.now()

        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def delete_session(
            db: Session,
            session_id: int,
            user_id: int,
            agent_id: int
    ):
        """
        删除会话，并级联删除该会话下所有聊天记录
        """
        session = SessionService.get_session(db, session_id, user_id, agent_id)

        # 删除关联的对话记录
        db.query(ChatHistory).filter(
            ChatHistory.agent_id == agent_id,
            ChatHistory.session_id == session.session_id
        ).delete()

        # 删除会话
        db.delete(session)
        db.commit()

        return {"detail": "会话删除成功"}