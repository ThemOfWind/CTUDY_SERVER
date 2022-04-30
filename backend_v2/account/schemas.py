from typing import List

from ninja import Schema, ModelSchema

from account.models import Member
from utils.response import ResponseSchema, PaginationSchema, SuccessStatus


# In Schema
class LoginSchema(Schema):
    username: str
    password: str


class SignupSchema(Schema):
    username: str
    password: str
    email: str
    name: str


# Out Schema
class UsernameCheck(Schema):
    username: str


class TokenSchema(Schema):
    access_token: str
    expires_in: int
    token_type: str
    scope: str
    refresh_token: str


class MemberSchema(ModelSchema):
    class Config:
        model = Member
        model_fields = ('id',
                        'name',
                        'username',
                        'image')


class MemberNameSchema(ModelSchema):
    class Config:
        model = Member
        model_fields = ('id',
                        'name',
                        'username')


class MemberPaginationSchema(PaginationSchema):
    items: List[MemberSchema]


class TokenResponse(ResponseSchema):
    response: TokenSchema


class ProfileResponse(ResponseSchema):
    response: MemberSchema


class UsernameCheckResponse(ResponseSchema):
    response: UsernameCheck


class MemberListResponse(ResponseSchema):
    response: MemberPaginationSchema
