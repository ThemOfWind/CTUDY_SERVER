from ninja import Schema


class ErrorMessage(Schema):
    message: str


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
    name: str


class ResponseSchema(Schema):
    result: bool
    response: dict
