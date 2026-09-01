from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from ..users.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    UserNotFoundException,
)
from ..users.models import Users
from .database import get_session
from .jwt import verify_token

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[Session, Depends(get_session)],
) -> Users:
    """Dependency to get the current authenticated user from JWT token."""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise InvalidTokenException()

    email: str = payload.get("sub")

    if not email:
        raise InvalidCredentialsException()

    statement = select(Users).where(Users.email == email)

    user = session.exec(statement).first()

    if user is None:
        raise UserNotFoundException(email)

    return user
