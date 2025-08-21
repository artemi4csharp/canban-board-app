from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ''
    column_id: int

class TaskOut(TaskCreate):
    id: int
    position: Optional[int] = None
    class Config:
        from_attributes = True