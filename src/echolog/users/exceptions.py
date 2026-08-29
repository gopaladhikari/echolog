from fastapi import Request
from fastapi.responses import JSONResponse


# Exceptions
class UserNotFoundException(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"User with email {email} not found")


class UserAlreadyExistsException(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"User with email {email} already exists")


class InvalidCredentialsException(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid credentials")


class InvalidTokenException(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid or expired token")


class IncorrectPasswordException(Exception):
    def __init__(self) -> None:
        super().__init__("Incorrect current password")


# Exceptions Handler
async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"User with email {exc.email} not found"},
    )


async def user_already_exists_exception_handler(
    request: Request, exc: UserAlreadyExistsException
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": f"User with email {exc.email} already exists"},
    )


async def invalid_credentials_exception_handler(
    request: Request, exc: InvalidCredentialsException
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid credentials"},
    )


async def invalid_token_exception_handler(
    request: Request, exc: InvalidTokenException
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid or expired token"},
    )


async def incorrect_password_exception_handler(
    request: Request, exc: IncorrectPasswordException
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": "Incorrect current password"},
    )
