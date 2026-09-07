from fastapi import status

from echolog.core.exceptions import APIException


# Exceptions
class UserNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, message: str = "User not found") -> None:
        super().__init__(message)


class UserAlreadyExistsException(APIException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(
        self, email: str, message: str = "User with email {email} already exists"
    ) -> None:
        self.email = email
        super().__init__(message.format(email=email))


class InvalidCredentialsException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, message: str = "Invalid email or password.") -> None:
        super().__init__(message)


class InvalidTokenException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, message: str = "Invalid or expired token") -> None:
        super().__init__(message)
