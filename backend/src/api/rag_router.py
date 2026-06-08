from typing import List

from core.db import get_db
from fastapi import APIRouter, Depends, UploadFile, File
from schemas.rag_schemas import RAGCreate, RAGResp
from services.rag_service import RAGService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/rag", tags=["RAG知识库接口"])

# ======================
# 1. 创建RAG知识库
# ======================
@router.post("", response_model=RAGResp)
def create_rag(
    req: RAGCreate,
    db: Session = Depends(get_db)
):
    return RAGService.create_rag(
        db=db,
        user_id=1,  # 这里以后从token拿，现在先写死测试
        name=req.name,
        description=req.description,
        avatar=req.avatar
    )

# ======================
# 2. 获取单个RAG知识库
# ======================
@router.get("/{rag_id}", response_model=RAGResp)
def get_rag(
    rag_id: int,
    db: Session = Depends(get_db)
):
    return RAGService.get_rag(
        db=db,
        user_id=1,  # 后续从token获取
        rag_id=rag_id
    )

# ======================
# 3. 获取当前用户所有RAG知识库
# ======================
@router.get("", response_model=List[RAGResp])
def get_user_rags(
    db: Session = Depends(get_db)
):
    return RAGService.get_user_rags(
        db=db,
        user_id=1  # 后续token替换
    )

# ======================
# 4. 更新RAG知识库
# ======================
@router.put("/{rag_id}", response_model=RAGResp)
def update_rag(
    rag_id: int,
    req: RAGCreate,
    db: Session = Depends(get_db)
):
    return RAGService.update_rag(
        db=db,
        user_id=1,
        rag_id=rag_id,
        name=req.name,
        description=req.description,
        avatar=req.avatar
    )

# ======================
# 5. 删除RAG知识库
# ======================
@router.delete("/{rag_id}")
def delete_rag(
    rag_id: int,
    db: Session = Depends(get_db)
):
    return RAGService.delete_rag(
        db=db,
        user_id=1,
        rag_id=rag_id
    )

# ======================
# 7. 上传文件到知识库
# ======================
@router.post("/{rag_id}/upload")
def upload_file_to_rag(
    rag_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    上传文件到指定知识库
    支持 txt、pdf 格式
    """
    return RAGService.upload_and_import_file(
        db=db,
        user_id=1,  # 后续从token获取
        rag_id=rag_id,
        file=file
    )