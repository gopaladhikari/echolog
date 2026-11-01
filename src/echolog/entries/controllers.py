from datetime import UTC, datetime

from sqlmodel import Session, func, select

from echolog.users.models import Users

from .exceptions import EntryNotFoundException, SubscriptionLimitExceededException
from .models import Entries
from .schemas import CreateEntry, UpdateEntry


class EntryController:
    """Controller for entry-related operations."""

    @staticmethod
    def create_entry(
        entry_data: CreateEntry, current_user: Users, session: Session
    ) -> Entries:
        """Create a new trading entry."""

        is_pro = (
            current_user.subscription is not None
            and current_user.subscription.status == "active"
        )

        if not is_pro:
            now = datetime.now(UTC)
            start_of_month = now.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )

            statement = select(func.count(Entries.id)).where(
                Entries.user_id == current_user.id, Entries.created_at >= start_of_month
            )

            monthly_count = session.exec(statement).one()

            if monthly_count >= 20:
                raise SubscriptionLimitExceededException()

        new_entry = Entries(
            user_id=current_user.id,
            instrument=entry_data.instrument,
            position_size=entry_data.position_size,
            entry_time=entry_data.entry_time,
            exit_time=entry_data.exit_time,
            pnl=entry_data.pnl,
            notes=entry_data.notes,
        )

        session.add(new_entry)
        session.commit()
        session.refresh(new_entry)

        return new_entry

    @staticmethod
    def get_entry_by_id(
        entry_id: int, current_user: Users, session: Session
    ) -> Entries:
        """Get an entry by ID, strictly scoped to the requesting user."""
        statement = select(Entries).where(
            Entries.id == entry_id, Entries.user_id == current_user.id
        )

        entry = session.exec(statement).first()

        if not entry:
            raise EntryNotFoundException(entry_id)

        return entry

    @staticmethod
    def get_all_entries(current_user: Users, session: Session) -> list[Entries]:
        """Get all entries explicitly scoped to the requesting user."""

        statement = select(Entries).where(Entries.user_id == current_user.id)

        statement = statement.order_by(Entries.entry_time.desc())

        entries = session.exec(statement).all()

        return entries

    @staticmethod
    def update_entry(
        entry_id: int, entry_data: UpdateEntry, current_user: Users, session: Session
    ) -> Entries:
        """Update an existing entry, strictly scoped to the requesting user."""

        entry = EntryController.get_entry_by_id(entry_id, current_user, session)

        entry_dict = entry_data.model_dump(exclude_unset=True)

        for key, value in entry_dict.items():
            setattr(entry, key, value)

        session.add(entry)
        session.commit()
        session.refresh(entry)

        return entry

    @staticmethod
    def delete_entry(entry_id: int, current_user: Users, session: Session) -> dict:
        """Delete an entry, strictly scoped to the requesting user."""

        entry = EntryController.get_entry_by_id(entry_id, current_user, session)

        session.delete(entry)
        session.commit()

        return {"message": "Entry deleted successfully"}
