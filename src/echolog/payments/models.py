from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from echolog.users.models import Users


class Subscription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    provider: str = Field(
        description="The payment gateway used (e.g., 'stripe', 'lemonsqueezy')"
    )

    provider_customer_id: str = Field(
        index=True, description="The external customer ID to match webhooks"
    )

    provider_subscription_id: str = Field(
        unique=True,
        index=True,
        description="The specific subscription ID from the gateway",
    )

    status: str = Field(
        index=True, description="e.g., 'active', 'past_due', 'canceled'"
    )

    plan_tier: str = Field(description="e.g., 'pro', 'elite'")

    current_period_end: datetime = Field(
        description="The exact date the current paid month ends"
    )

    cancel_at_period_end: bool = Field(
        default=False,
        description="True if the user canceled but still has remaining time",
    )

    user_id: int = Field(foreign_key="users.id", nullable=False, unique=True)

    user: Users = Relationship(back_populates="subscription")

    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"server_default": func.now()},
    )

    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
    )
