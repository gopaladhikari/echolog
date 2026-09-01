from sqlmodel import Session, select

from .exceptions import EntryNotFoundException
from .models import Entries
from .schemas import CreateEntry, UpdateEntry


class EntryController:
    """Controller for entry-related operations."""

    @staticmethod
    def create_entry(
        entry_data: CreateEntry, user_id: int, session: Session
    ) -> Entries:
        """Create a new trading entry."""
        new_entry = Entries(
            user_id=user_id,
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
    def get_entry_by_id(entry_id: int, user_id: int, session: Session) -> Entries:
        """Get an entry by ID for a specific user."""
        statement = select(Entries).where(
            Entries.id == entry_id, Entries.user_id == user_id
        )
        entry = session.exec(statement).first()

        if not entry:
            raise EntryNotFoundException(entry_id)

        return entry

    @staticmethod
    def get_all_entries(user_id: int, session: Session) -> list[Entries]:
        """Get all entries for a specific user."""
        statement = select(Entries).where(Entries.user_id == user_id)
        entries = session.exec(statement).all()
        return entries

    @staticmethod
    def update_entry(
        entry_id: int, entry_data: UpdateEntry, user_id: int, session: Session
    ) -> Entries:
        """Update an existing entry."""
        entry = EntryController.get_entry_by_id(entry_id, user_id, session)

        if entry_data.instrument is not None:
            entry.instrument = entry_data.instrument
        if entry_data.position_size is not None:
            entry.position_size = entry_data.position_size
        if entry_data.entry_time is not None:
            entry.entry_time = entry_data.entry_time
        if entry_data.exit_time is not None:
            entry.exit_time = entry_data.exit_time
        if entry_data.pnl is not None:
            entry.pnl = entry_data.pnl
        if entry_data.notes is not None:
            entry.notes = entry_data.notes

        session.add(entry)
        session.commit()
        session.refresh(entry)

        return entry

    @staticmethod
    def delete_entry(entry_id: int, user_id: int, session: Session) -> dict:
        """Delete an entry."""
        entry = EntryController.get_entry_by_id(entry_id, user_id, session)

        session.delete(entry)
        session.commit()

        return {"message": "Entry deleted successfully"}
