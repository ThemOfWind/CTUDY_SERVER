import datetime
from typing import List

from ninja import Schema, ModelSchema

from account.schemas import MemberNameSchema
from coupon.models import Coupon
from utils.response import ResponseSchema


# Core Schema
class CouponSchema(ModelSchema):
    sender: MemberNameSchema
    receiver: MemberNameSchema

    class Config:
        model = Coupon
        model_fields = ('id',
                        'name',
                        'start_date',
                        'end_date',
                        'sender',
                        'receiver')


# In Schema
class CouponCreateIn(Schema):
    name: str
    room_id: int
    receiver_id: int
    start_date: str
    end_date: str


# Out Schema
class CouponReturnSchema(Schema):
    send_list: List[CouponSchema] = None
    receive_list: List[CouponSchema] = None


class CouponListResponse(ResponseSchema):
    response: CouponReturnSchema
