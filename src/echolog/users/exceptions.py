from fastapi import status

from echolog.core.exceptions import APIException


# Exceptions
class UserNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"User with email {email} not found")


class UserAlreadyExistsException(APIException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"User with email {email} already exists")


class InvalidCredentialsException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self) -> None:
        super().__init__("Invalid credentials")


class InvalidTokenException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self) -> None:
        super().__init__("Invalid or expired token")


class IncorrectPasswordException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self) -> None:
        super().__init__("Incorrect current password")
