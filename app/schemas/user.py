from pydantic import BaseModel
from app.schemas.task import TaskResponse

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    tasks: list[TaskResponse]

    class Config:
        from_attributes = True