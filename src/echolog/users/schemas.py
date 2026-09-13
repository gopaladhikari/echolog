from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from .exceptions import InvalidPasswordException


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
    full_name: str = Field(..., min_length=3, max_length=30)


class Login(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "user@echolog.com", "password": "Echolog123"}
        }
    )


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
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @field_validator("confirm_password")
    def passwords_match(cls, v: str, info: FieldValidationInfo) -> str:
        if v != info.data.get("new_password"):
            raise InvalidPasswordException()
        return v
