from fastapi import Request, status
from fastapi.responses import JSONResponse


class APIException(Exception):
    """Base exception for managing status codes and error messages."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str) -> None:
        super().__init__(message)


async def global_api_exception_handler(
    request: Request, exc: APIException
) -> JSONResponse:
    """Catches any subclass of APIException and formats a clean JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc)},
    )
