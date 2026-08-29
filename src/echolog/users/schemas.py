from datetime import datetime

from pydantic import BaseModel


class CreateUser(BaseModel):
    full_name: str
    email: str
    password: str


class ReadUser(BaseModel):
    id: int
    full_name: str
    email: str
    created_at: datetime
    updated_at: datetime


class UpdateUser(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None
