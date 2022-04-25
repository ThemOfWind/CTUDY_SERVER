from typing import List

from ninja import Schema, ModelSchema

from account.schemas import MemberSchema
from room.models import Room
from utils.response import ResponseSchema


class ErrorMessage(Schema):
    message: str


class SuccessStatus(Schema):
    success: bool


class PostSuccess(Schema):
    id: str


class RoomCreateIn(Schema):
    name: str


class RoomUpdateIn(Schema):
    name: str = None
    master: int = None


class RoomSchema(ModelSchema):
    class Config:
        model = Room
        model_fields = ('id',
                        'name',
                        'banner')


class RoomListSchema(Schema):
    id: int
    name: str
    banner: str = None
    member_count: int
    master_name: str


class RoomDetailSchema(Schema):
    id: int
    name: str
    members: List[MemberSchema]
    master: MemberSchema


class RoomListResponse(ResponseSchema):
    response: List[RoomListSchema]


class RoomDetailResponse(ResponseSchema):
    response: RoomDetailSchema


class RoomIdResponse(ResponseSchema):
    response: PostSuccess


class SuccessResponse(ResponseSchema):
    response: SuccessStatus
