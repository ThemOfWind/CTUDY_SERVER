from typing import Any

from ninja import Schema


class SuccessStatus(Schema):
    success: bool


class PostSuccess(Schema):
    id: str


class ResponseSchema(Schema):
    result: bool
    response: Any


class PaginationSchema(Schema):
    count: int
    next: str = None
    previous: str = None
    items: Any


class ErrorMessage(Schema):
    message: str


class ErrorResponseSchema(Schema):
    result: bool = False
    error: ErrorMessage


class SuccessResponse(ResponseSchema):
    response: SuccessStatus
