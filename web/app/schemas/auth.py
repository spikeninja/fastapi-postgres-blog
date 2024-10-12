from typing import Literal

from pydantic import BaseModel, EmailStr, Field

from app.schemas.users import UserPublic


class TwoFAResponse(BaseModel):
    user_id: str
    two_fa: bool


class SendCodeRequest(BaseModel):
    user_id: str
    send_method: Literal['email']


class CodeRequest(BaseModel):
    user_id: str
    code: str


class AuthResponse(BaseModel):
    token: str
    user: UserPublic


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    repeat_password: str = Field(min_length=8)


class ChangePassword(BaseModel):
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
