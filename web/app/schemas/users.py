from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserDTO(BaseModel):
    id: int
    name: str
    email: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None


class UserPublic(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    name: str | None = None


class PasswordUpdate(BaseModel):
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
