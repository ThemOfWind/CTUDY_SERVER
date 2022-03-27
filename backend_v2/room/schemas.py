from ninja import Schema, ModelSchema

from room.models import Room


class ErrorMessage(Schema):
    message: str


class SuccessStatus(Schema):
    success: bool


class PostSuccess(Schema):
    id: str


class RoomSchemaIn(Schema):
    name: str


class RoomSchema(ModelSchema):
    class Config:
        model = Room
        model_fields = '__all__'
