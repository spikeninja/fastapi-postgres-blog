from datetime import datetime

from pydantic import BaseModel


class CommentUser(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class CommentPost(BaseModel):
    id: int
    user_id: int
    author: CommentUser
    created_at: datetime
    updated_at: datetime


class CommentDTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    text: str
    user_id: int
    post_id: int
    post: CommentPost
    author: CommentUser


class CommentPublic(CommentDTO):
    pass


# Requests
class CommentCreateRequest(BaseModel):
    text: str


class CommentUpdateRequest(BaseModel):
    text: str | None = None
