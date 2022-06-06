from typing import List

from ninja import Schema, ModelSchema

from account.schemas import MemberSchema, RoomMemberSchema
from room.models import Room
from utils.response import ResponseSchema, PostSuccess, SuccessStatus


# Core Schema
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
    master_username: str


class RoomDetailSchema(Schema):
    id: int
    name: str
    banner: str = None
    members: List[RoomMemberSchema]
    master: RoomMemberSchema


# In Schema
class RoomCreateIn(Schema):
    name: str
    member_list: List[int]


class RoomUpdateIn(Schema):
    name: str = None
    master: int = None


class MemberIn(Schema):
    member_list: List[int]


# Out Schema
class RoomListResponse(ResponseSchema):
    response: List[RoomListSchema]


class RoomDetailResponse(ResponseSchema):
    response: RoomDetailSchema


class RoomIdResponse(ResponseSchema):
    response: PostSuccess
