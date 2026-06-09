# api/tool_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from services.tool_service import ToolService
from schemas.tool_schemas import ToolResp

router = APIRouter(prefix="/tools", tags=["工具管理"])


@router.get("", response_model=list[ToolResp])
def get_all_tools(db: Session = Depends(get_db)):
    """获取所有可用工具（用于前端显示）"""
    return ToolService.get_all_tools(db)
