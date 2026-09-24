from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class CreateEntry(BaseModel):
    instrument: str = Field(..., min_length=1, max_length=15)
    position_size: float = Field(..., gt=0)
    entry_time: datetime
    exit_time: datetime | None = None
    pnl: float | None = None
    notes: str = Field(..., min_length=1)

    @field_validator("instrument")
    @classmethod
    def format_instrument(cls, v: str) -> str:
        return v.strip().upper()


class ReadEntry(BaseModel):
    id: int
    instrument: str
    position_size: float
    entry_time: datetime
    exit_time: datetime | None
    pnl: float | None
    notes: str
    created_at: datetime
    updated_at: datetime


class UpdateEntry(BaseModel):
    instrument: str | None = Field(None, min_length=1, max_length=15)
    position_size: float | None = Field(None, gt=0)
    entry_time: datetime | None = None
    exit_time: datetime | None = None
    pnl: float | None = None
    notes: str | None = Field(None, min_length=1)
