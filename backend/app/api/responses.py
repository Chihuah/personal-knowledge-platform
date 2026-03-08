from typing import Any, Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class APIError(BaseModel):
    code: str
    message: str
    details: Any | None = None


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T


class ErrorResponse(BaseModel):
    success: bool = False
    error: APIError


def success_response(data: T) -> SuccessResponse[T]:
    return SuccessResponse[T](data=data)


def error_response(code: str, message: str, details: Any | None = None) -> ErrorResponse:
    return ErrorResponse(error=APIError(code=code, message=message, details=details))
