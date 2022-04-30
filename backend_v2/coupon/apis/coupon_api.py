import datetime
import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router

from coupon.models import Coupon
from coupon.schemas import CouponListResponse, CouponCreateIn

from settings.auth import AuthBearer, auth_check
from utils.base import base_api
from utils.error import error_codes
from utils.response import ErrorResponseSchema, SuccessResponse

router = Router(tags=['Coupon'])
logger = logging.getLogger('coupon')


@router.get("/", response={200: CouponListResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def list_coupon(request, room_id: int, mode: str = 'a'):
    if mode == 's':
        coupon_list = Coupon.objects.filter(sender=request.user, room_id=room_id, is_use=False)
        return_data = {
            'send_list': list(coupon_list),
            'receive_list': []
        }
    elif mode == 'r':
        coupon_list = Coupon.objects.filter(receiver=request.user, room_id=room_id, is_use=False)
        return_data = {
            'send_list': [],
            'receive_list': list(coupon_list)
        }
    else:
        coupon_list = Coupon.objects.filter(Q(sender=request.user) | Q(receiver=request.user),
                                            room_id=room_id, is_use=False)
        return_data = {
            'send_list': list(),
            'receive_list': list()
        }

        for coupon in coupon_list:
            if coupon.receiver == request.user:
                return_data['receive_list'].append(coupon)
            elif coupon.sender == request.user:
                return_data['send_list'].append(coupon)
            else:
                continue

    return return_data


@router.post("/", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def create_coupon(request, payload: CouponCreateIn):
    payload_data = payload.dict()
    payload_data['sender'] = request.user

    Coupon.objects.create(**payload_data)
    return {'success': True}


@router.delete("/{coupon_id}", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def use_coupon(request, coupon_id: str):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    coupon.is_use = True
    coupon.used_time = datetime.datetime.now()
    coupon.save()

    return {'success': True}
