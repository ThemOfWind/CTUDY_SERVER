from typing import List

from ninja import Schema, ModelSchema

from account.models import Member
from utils.response import ResponseSchema, PaginationSchema


# In Schema
class LoginSchema(Schema):
    username: str
    password: str


class SignupSchema(Schema):
    username: str
    password: str
    email: str
    name: str


class FindIdSchema(Schema):
    email: str


class FindPwSchema(Schema):
    email: str
    username: str


class CertificateSchema(Schema):
    email: str
    username: str
    code: str
    key: str


class ProfileNameSchema(Schema):
    name: str


# Out Schema
class UsernameCheck(Schema):
    username: str


class SignupSuccess(Schema):
    username: str
    name: str


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


class RoomMemberSchema(ModelSchema):
    coupon: int = 0

    class Config:
        model = Member
        model_fields = ('id',
                        'name',
                        'username',
                        'image')


class CertificateKeySchema(Schema):
    key: str


class MemberPaginationSchema(PaginationSchema):
    items: List[MemberSchema]


class TokenResponse(ResponseSchema):
    response: TokenSchema


class ProfileResponse(ResponseSchema):
    response: MemberSchema


class UsernameCheckResponse(ResponseSchema):
    response: UsernameCheck


class SignupSuccessResponse(ResponseSchema):
    response: SignupSuccess


class MemberListResponse(ResponseSchema):
    response: MemberPaginationSchema


class CertificateKeyResponse(ResponseSchema):
    response: CertificateKeySchema
