from ninja import Schema

from utils.common import ResponseSchema


class SuccessStatus(Schema):
    success: bool


class PostSuccess(Schema):
    id: str


class LoginSchema(Schema):
    username: str
    password: str


class SignupSchema(Schema):
    username: str
    password: str
    email: str
    name: str


class TokenSchema(Schema):
    access_token: str
    expires_in: int
    token_type: str
    scope: str
    refresh_token: str


class SuccessStatusResponse(ResponseSchema):
    response: SuccessStatus


class TokenResponse(ResponseSchema):
    response: TokenSchema
