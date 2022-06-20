import datetime
import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router, UploadedFile

from account.models import Member
from coupon.models import Coupon
from room.models import Room, RoomConfig
from room.schemas import RoomSchema, RoomCreateIn, RoomUpdateIn, RoomIdResponse, RoomListResponse, RoomDetailResponse
from settings.auth import AuthBearer, auth_check, master_check
from utils.base import base_api
from utils.error import error_codes, CtudyException, param_error_return, not_found_error_return
from utils.response import ErrorResponseSchema, SuccessResponse

router = Router(tags=['Study - Room'])
logger = logging.getLogger('room')


@router.get("/", response={200: RoomListResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def list_room(request):
    room_list = Room.objects.filter(
        Q(members=request.user) | Q(roomconfig__master=request.user),
        is_deleted=False
    ).distinct()
    result = list()
    for room in room_list:
        result.append({
            **RoomSchema.validate(room).dict(),
            'member_count': room.members.count() + 1,
            'master_name': room.roomconfig.master.name,
            'master_username': room.roomconfig.master.username
        })

    return result


@router.post("/", response={200: RoomIdResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def create_room(request, payload: RoomCreateIn, file: UploadedFile = None):
    payload_data = payload.dict()

    if file is not None:
        payload_data['banner'] = file

    member_list = payload_data.pop('member_list')

    room = Room.objects.create(**payload_data)
    if len(member_list) > 0:
        q = Q()
        [q.add(Q(id=member_id), Q.OR) for member_id in member_list if member_id != request.user.id]
        if len(q) > 0:
            member_list = Member.objects.filter(q)
            room.members.add(*member_list)
            room.save()

    RoomConfig.objects.create(room=room, master=request.user)

    return {'id': room.id}


@router.get("/{room_id}", response={200: RoomDetailResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def get_room(request, room_id: str):
    room = get_object_or_404(Room, id=room_id, is_deleted=False)
    if not room.members.filter(id=request.user.id).exists() and room.roomconfig.master != request.user:
        raise CtudyException(404, not_found_error_return)
    members = list()

    now = datetime.datetime.now().date()
    for member in room.members.all():
        member.coupon = Coupon.objects.filter(receiver=request.user,
                                              start_date__lte=now,
                                              end_date__gte=now,
                                              room_id=room_id,
                                              is_use=False).count()
        members.append(member)

    master = room.roomconfig.master
    master.coupon = Coupon.objects.filter(room=room, receiver=master).count()

    result = {
        **RoomSchema.validate(room).dict(),
        'members': members,
        'master': master
    }

    return result


@router.delete("/{room_id}/member/{member_id}",
               response={200: SuccessResponse, error_codes: ErrorResponseSchema},
               auth=AuthBearer())
@base_api(logger)
@auth_check
def out_room(request, room_id: int, member_id: int):
    room = get_object_or_404(Room, id=room_id, is_deleted=False)
    if request.user.id != member_id or room.roomconfig.master == request.user:
        raise CtudyException(400, param_error_return)

    Coupon.objects.filter(receiver=request.user, room=room).delete()
    room.members.remove(request.user)

    return {'success': True}


@router.put("/{room_id}", response={200: RoomIdResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
@master_check
def update_room(request, room_id: str, payload: RoomUpdateIn):
    room = get_object_or_404(Room, id=room_id)
    payload_data = payload.dict()

    for attr, value in payload_data.items():
        if value is not None:
            if attr == 'master':
                member = room.members.filter(id=value)
                if member.exists():
                    member = member[0]
                    room.members.remove(member)
                    room.members.add(request.user)
                    room.save()
                    room.roomconfig.master = member
                    room.roomconfig.save()
            else:
                setattr(room, attr, value)
                room.save()

    return {'id': room.id}


@router.post("/banner/{room_id}", response={200: RoomIdResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
@master_check
def update_banner_room(request, room_id: str, file: UploadedFile = None):
    room = get_object_or_404(Room, id=room_id)
    room.banner = file
    room.save()

    return {'id': room.id}


@router.delete("/{room_id}", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
@master_check
def delete_room(request, room_id: str):

    room = get_object_or_404(Room, id=room_id)
    room.is_deleted = True
    room.deleted_time = datetime.datetime.now()
    room.save()

    return {'success': True}
