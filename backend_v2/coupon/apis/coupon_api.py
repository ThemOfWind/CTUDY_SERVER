import datetime
import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router, UploadedFile

from coupon.models import Coupon
from coupon.schemas import CouponListResponse, CouponCreateIn

from settings.auth import AuthBearer, auth_check
from utils.base import base_api
from utils.error import error_codes, CtudyException, not_found_error_return
from utils.response import ErrorResponseSchema, SuccessResponse

router = Router(tags=['Coupon'])
logger = logging.getLogger('coupon')


@router.get("/", response={200: CouponListResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def list_coupon(request, room_id: int, mode: str = 'a'):
    if mode == 'a':
        coupon_list = Coupon.objects.filter(Q(sender=request.user) | Q(receiver=request.user),
                                            room_id=room_id, is_use=False).order_by('-created_date')
    elif mode == 'r':
        now = datetime.datetime.now().date()
        coupon_list = Coupon.objects.filter(receiver=request.user,
                                            start_date__lte=now,
                                            end_date__gte=now,
                                            room_id=room_id, is_use=False).order_by('-created_date')
    elif mode == 'rd':
        now = datetime.datetime.now()
        coupon_list = Coupon.objects.filter(receiver=request.user,
                                            end_date__lt=now.date(),
                                            room_id=room_id, is_use=False).order_by('-created_date')
    else:
        raise CtudyException(404, not_found_error_return)

    return list(coupon_list)


@router.post("/", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def create_coupon(request, payload: CouponCreateIn, file: UploadedFile = None):
    payload_data = payload.dict()
    if file is not None:
        payload_data['banner'] = file
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
