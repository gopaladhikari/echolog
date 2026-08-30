from fastapi import APIRouter, Depends, status
from sqlmodel import Session


from ..core.database import get_session


entries_router = APIRouter(
    prefix="/entries", tags=["Entries"], description="Entry management endpoints"
)
