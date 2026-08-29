from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)


class ReadUser(BaseModel):
    id: int
    full_name: str
    email: str
    created_at: datetime
    updated_at: datetime


class UpdateUser(BaseModel):
    full_name: str | None = Field(None, min_length=3, max_length=30)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8)


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None


class ChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
