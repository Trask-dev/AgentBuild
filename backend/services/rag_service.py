import os
import shutil
from sqlalchemy.orm import Session
from ai.rag.vector_store import VectorStoreService
from ai.utils.config_handler import chroma_conf
from ai.utils.logger_handler import logger
from ai.utils.path_tool import get_abs_path
from models.rag_model import RAG
from fastapi import HTTPException, UploadFile


class RAGService:
    @staticmethod
    def create_rag(
            db: Session,
            user_id: int,
            name: str,
            description: str = None,
            avatar: str = None
    ):
        """
        创建 RAG 知识库
        """
        db_rag = RAG(
            user_id=user_id,
            name=name,
            description=description,
            avatar=avatar
        )
        db.add(db_rag)
        db.commit()
        db.refresh(db_rag)
        return db_rag

    @staticmethod
    def get_rag(
            db: Session,
            user_id: int,
            rag_id: int
    ):
        """
        获取单个 RAG 知识库
        """
        rag = db.query(RAG).filter(
            RAG.id == rag_id,
            RAG.user_id == user_id
        ).first()

        if not rag:
            raise HTTPException(status_code=404, detail="RAG知识库不存在")
        return rag

    @staticmethod
    def get_user_rags(
            db: Session,
            user_id: int
    ):
        """
        获取当前用户所有 RAG 知识库
        """
        return db.query(RAG).filter(RAG.user_id == user_id).all()

    @staticmethod
    def update_rag(
            db: Session,
            user_id: int,
            rag_id: int,
            name: str,
            description: str = None,
            avatar: str = None
    ):
        """
        更新 RAG 知识库
        """
        rag = RAGService.get_rag(db, user_id, rag_id)

        rag.name = name
        rag.description = description
        rag.avatar = avatar

        db.commit()
        db.refresh(rag)
        return rag

    @staticmethod
    def delete_rag(
            db: Session,
            user_id: int,
            rag_id: int
    ):
        """
        删除 RAG 知识库
        """
        rag = RAGService.get_rag(db, user_id, rag_id)
        db.delete(rag)
        db.commit()
        return {"detail": "删除成功"}

    @staticmethod
    def upload_and_import_file(
            db: Session,
            user_id: int,
            rag_id: int,
            file: UploadFile
    ):
        """
        上传文件并自动导入向量库（简洁版，自带文件防重）
        1. 验证知识库
        2. 验证文件类型
        3. 保存文件（同名自动重命名，不覆盖）
        4. 自动导入向量库
        """
        # 1. 验证知识库是否存在
        RAGService.get_rag(db, user_id, rag_id)

        # 2. 验证文件类型
        allowed_types = chroma_conf.get("allow_knowledge_file_type", ["txt", "pdf"])
        file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
        if file_ext not in allowed_types:
            raise HTTPException(status_code=400, detail=f"仅支持: {', '.join(allowed_types)}")

        # 3. 构建目录
        target_dir = get_abs_path(f"{chroma_conf['data_path']}/kb_{rag_id}")
        os.makedirs(target_dir, exist_ok=True)

        # 4. 防重保存文件（核心：自动重命名，绝不覆盖）
        name, ext = os.path.splitext(file.filename)
        save_path = os.path.join(target_dir, file.filename)
        count = 1
        while os.path.exists(save_path):
            save_path = os.path.join(target_dir, f"{name}({count}){ext}")
            count += 1

        # 保存文件
        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # 5. 导入向量库
        try:
            vs = VectorStoreService(kb_id=rag_id)
            vs.load_documents()
        except Exception as e:
            logger.error(f"向量库导入失败: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"文件上传成功，但导入向量库失败")

        return {
            "detail": "上传并导入成功",
            "filename": os.path.basename(save_path)
        }