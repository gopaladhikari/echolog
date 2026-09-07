from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import APIKeyCookie
from sqlmodel import Session, select

from ..users.exceptions import (
    InvalidTokenException,
    UserNotFoundException,
)
from ..users.models import Users
from .database import get_session
from .jwt import verify_token

cookie_scheme = APIKeyCookie(name="access_token")


async def get_current_user(
    token: Annotated[str | None, Depends(cookie_scheme)],
    session: Annotated[Session, Depends(get_session)],
) -> Users:
    """Dependency to get the current authenticated user from JWT token."""
    if not token:
        raise InvalidTokenException()
    try:
        payload = verify_token(token)

        statement = select(Users).where(Users.email == payload.email)

        user = session.exec(statement).first()

        if user is None:
            raise UserNotFoundException(payload.email)

        return user
    except jwt.PyJWTError:
        raise InvalidTokenException()
