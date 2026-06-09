from models.tool_model import Tool
from sqlalchemy.orm import Session


class ToolService:
    @staticmethod
    def get_all_tools(db: Session) -> list[Tool]:
        """获取所有可用工具"""
        return db.query(Tool).all()

    @staticmethod
    def validate_tool_names(db: Session, tool_names: list[str]) -> bool:
        """验证工具名称是否有效"""
        if not tool_names:
            return True

        # 查询数据库中存在的工具名称
        existing_tools = db.query(Tool.name).filter(Tool.name.in_(tool_names)).all()
        existing_names = {name[0] for name in existing_tools}

        # 检查是否有无效的工具名称
        invalid_names = set(tool_names) - existing_names
        return len(invalid_names) == 0
