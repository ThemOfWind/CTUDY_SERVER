from typing import List

from ninja import Schema, ModelSchema

from account.schemas import MemberSchema
from coupon.models import Coupon
from utils.response import ResponseSchema


# Core Schema
class CouponSchema(ModelSchema):
    sender: MemberSchema
    receiver: MemberSchema

    class Config:
        model = Coupon
        model_fields = ('id',
                        'name',
                        'sender',
                        'receiver',
                        'image',
                        'start_date',
                        'end_date')


# In Schema
class CouponCreateIn(Schema):
    name: str
    room_id: int
    receiver_id: int
    start_date: str
    end_date: str


# Out Schema
class CouponListResponse(ResponseSchema):
    response: List[CouponSchema]
