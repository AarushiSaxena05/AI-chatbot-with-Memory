from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: Optional[str] = None
    interests: Optional[str] = None
    skills: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: Optional[str]
    interests: Optional[str]
    skills: Optional[str]

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    user_id: int
    content: str


class MessageResponse(BaseModel):
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True