from typing import List

from ninja import Schema


class ErrorMessage(Schema):
    message: str


class SuccessStatus(Schema):
    success: bool


class PostSuccess(Schema):
    id: str


class PostMemberSchemaIn(Schema):
    member_list: List[int]
