from datetime import datetime

from pydantic import BaseModel
from app.schemas.users import UserDTO, UserPublic


class PostDTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    text: str
    title: str
    tags: list[str]
    user_id: int
    likes_count: int
    author: UserDTO


class PostPublic(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    text: str
    title: str
    tags: list[str]
    likes_count: int
    author: UserPublic


# Requests
class PostCreateRequest(BaseModel):
    text: str
    title: str
    tags: list[str]


class PostUpdateRequest(BaseModel):
    text: str | None = None
    title: str | None = None
    tags: list[str] | None = None
