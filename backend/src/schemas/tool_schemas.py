from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ToolBase(BaseModel):
    name: str
    description: Optional[str] = None


class ToolCreate(ToolBase):
    pass


class ToolResp(ToolBase):
    id: int
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True
