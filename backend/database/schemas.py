from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    name: str


class TaskCreate(BaseModel):
    user_id: int
    task_name: str


class TaskResult(BaseModel):
    task_id: int
    result_text: str
