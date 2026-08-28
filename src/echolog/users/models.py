from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime
from typing import Optional


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    full_name: str = Field(
        ...,
        max_length=30,
        min_length=3,
        nullable=False,
        description="User's full name",
    )

    email: str = Field(
        ...,
        max_length=50,
        min_length=3,
        nullable=False,
        unique=True,
        index=True,
        description="User's email address",
    )

    password: str = Field(
        ..., min_length=8, nullable=False, description="User's password"
    )

    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )

    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
    )

    history_analyses: list["HistoryAnalysis"] = Relationship(back_populates="user")

    subscription: Optional["Subscription"] = Relationship(back_populates="user")
