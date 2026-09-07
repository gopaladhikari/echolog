from datetime import UTC, datetime, timedelta

from jwt import decode, encode
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from echolog.users.exceptions import InvalidTokenException

from .config import config


class JWT(BaseModel):
    id: int
    email: str


def create_access_token(data: JWT, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.model_dump()

    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = encode(
        to_encode, config.ACCESS_TOKEN_SECRET_KEY, algorithm=config.ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> JWT:
    """Verify a JWT token and return the payload."""
    try:
        payload = decode(
            token, config.ACCESS_TOKEN_SECRET_KEY, algorithms=[config.ALGORITHM]
        )

        return JWT(**payload)

    except InvalidTokenError:
        raise InvalidTokenException()
