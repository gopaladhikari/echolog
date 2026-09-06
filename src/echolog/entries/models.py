from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, func

if TYPE_CHECKING:
    from echolog.users.models import Users


class Entries(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id")

    instrument: str = Field(
        ...,
        max_length=15,
        index=True,
        nullable=False,
        description="The traded asset (e.g., XAUUSD, BTCUSDT)",
    )

    position_size: float = Field(
        ..., description="The lot size or contract amount used"
    )

    entry_time: datetime = Field(
        ..., description="Exact date and time the position was opened"
    )

    exit_time: datetime | None = Field(
        default=None, description="Exact date and time the position was closed"
    )

    pnl: float | None = Field(
        default=None, description="Profit or loss for tracking evaluation metrics"
    )

    notes: str = Field(
        ...,
        description="Your raw thoughts on the setup, execution, and emotions",
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"server_default": func.now()},
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
    )

    user: "Users" = Relationship(back_populates="entries")  # noqa
