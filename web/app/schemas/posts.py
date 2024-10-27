from datetime import datetime

from pydantic import BaseModel
from app.schemas.users import UserDTO, UserPublic


class PostDTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    text: str
    title: str
    user_id: int
    is_liked: bool
    tags: list[str]
    author: UserDTO
    likes_count: int


class PostPublic(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    text: str
    title: str
    is_liked: bool
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
