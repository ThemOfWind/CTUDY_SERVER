from typing import Any

from ninja import Schema


class ResponseSchema(Schema):
    result: bool
    response: Any


class ErrorMessage(Schema):
    message: str


class ErrorResponseSchema(Schema):
    result: bool = False
    error: ErrorMessage
