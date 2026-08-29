from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from echolog.entries.models import Entries
    from echolog.users.models import Users


class TradeAnalysis(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    summary: str = Field(description="AI generated summary of the trade")

    mood_tag: str = Field(description="Psychological state extracted by AI")

    entry_id: int = Field(foreign_key="entries.id", nullable=False)

    entry: Entries = Relationship(back_populates="analyses")

    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"server_default": func.now()},
    )


class HistoryAnalysis(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    timeframe_start: datetime = Field(description="Start of the analyzed period")

    timeframe_end: datetime = Field(description="End of the analyzed period")

    overall_summary: str = Field(description="AI review of the entire week/month")

    dominant_emotion: str = Field(description="e.g., Overconfident, Disciplined")

    user_id: int = Field(foreign_key="users.id", nullable=False)

    user: Users = Relationship(back_populates="history_analyses")
