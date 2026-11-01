from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from ..core.database import get_session
from ..core.dependencies import get_current_user
from ..users.models import Users
from .controllers import EntryController
from .schemas import CreateEntry, ReadEntry, UpdateEntry

entries_router = APIRouter(prefix="/entries", tags=["Entries"])


CurrentUser = Annotated[Users, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_session)]


@entries_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReadEntry)
def create_entry(
    entry_data: CreateEntry,
    current_user: CurrentUser,
    session: DB,
):
    """Create a new trading entry."""
    return EntryController.create_entry(entry_data, current_user, session)


@entries_router.get("/", response_model=list[ReadEntry])
def get_entries(
    current_user: CurrentUser,
    session: DB,
):
    """Get all entries for the current user."""
    return EntryController.get_all_entries(current_user.id, session)


@entries_router.get("/{entry_id}", response_model=ReadEntry)
def get_entry(
    entry_id: int,
    current_user: CurrentUser,
    session: DB,
):
    """Get a specific entry by ID."""
    return EntryController.get_entry_by_id(entry_id, session)


@entries_router.patch("/{entry_id}", response_model=ReadEntry)
def update_entry(
    entry_id: int,
    entry_data: UpdateEntry,
    current_user: CurrentUser,
    session: DB,
):
    """Update an existing entry."""
    return EntryController.update_entry(entry_id, entry_data, session)


@entries_router.delete("/{entry_id}")
def delete_entry(
    entry_id: int,
    current_user: CurrentUser,
    session: DB,
):
    """Delete an entry."""
    return EntryController.delete_entry(entry_id, session)
