from datetime import UTC, datetime, timedelta

from jwt import decode, encode
from jwt.exceptions import InvalidTokenError

from .config import config


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = encode(
        to_encode, config.ACCESS_TOKEN_SECRET_KEY, algorithm=config.ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> dict | str:
    """Verify a JWT token and return the payload."""
    try:
        payload = decode(
            token, config.ACCESS_TOKEN_SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        return payload

    except InvalidTokenError as e:
        return str(e)
