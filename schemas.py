from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    completed: bool = False

class TaskCreate(TaskBase):
    id: str
    updatedAt: datetime

class TaskUpdate(TaskBase):
    updatedAt: datetime

class TaskResponse(TaskBase):
    id: str
    updatedAt: datetime

    class Config:
        orm_mode = True
