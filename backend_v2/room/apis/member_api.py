import logging
from typing import List

from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from account.models import Member
from account.schemas import MemberSchema
from room.models import Room
from room.schemas import MemberIn
from settings.auth import AuthBearer, auth_check, master_check
from utils.base import base_api
from utils.pagination import PageNumberPaginationExtra
from utils.response import ErrorResponseSchema, SuccessResponse
from utils.error import error_codes, server_error_return, CtudyException, not_found_error_return

router = Router(tags=['Study - Member'])
logger = logging.getLogger('member')


@router.get("/", response={200: List[MemberSchema], error_codes: ErrorResponseSchema}, auth=AuthBearer())
@auth_check
@paginate(PageNumberPaginationExtra)
def list_member(request):
    try:
        return 200, Member.objects.all()
    except Exception as e:
        logger.error(e.__str__())
        raise CtudyException(500, server_error_return)


@router.post("/{room_id}", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
@master_check
def join_member(request, room_id: str, payload: MemberIn):
    payload_data = payload.dict()
    room = get_object_or_404(Room, id=room_id)
    q = Q()
    [q.add(Q(id=member_id), Q.OR) for member_id in payload_data['member_list'] if member_id != request.user.id]

    if len(q) <= 0:
        raise CtudyException(401, not_found_error_return)

    member_list = Member.objects.filter(q)
    room.members.add(*member_list)
    room.save()

    return {'success': True}


@router.delete("/{room_id}", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
@master_check
def delete_member(request, room_id: str, payload: MemberIn):
    payload_data = payload.dict()
    room = get_object_or_404(Room, id=room_id)
    q = Q()
    [q.add(Q(id=member_id), Q.OR) for member_id in payload_data['member_list'] if member_id != request.user.id]

    if len(q) <= 0:
        raise CtudyException(401, not_found_error_return)

    member_list = Member.objects.filter(q)
    room.members.remove(*member_list)
    room.save()

    return {'success': True}
