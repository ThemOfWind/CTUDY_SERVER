from ninja import Schema, ModelSchema

from account.models import Member
from utils.response import ResponseSchema


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
class SuccessStatus(Schema):
    success: bool


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


class SuccessStatusResponse(ResponseSchema):
    response: SuccessStatus


class TokenResponse(ResponseSchema):
    response: TokenSchema
