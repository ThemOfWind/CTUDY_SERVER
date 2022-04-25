import datetime
import logging

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router, UploadedFile

from account.models import Member
from room.models import Room, RoomConfig
from room.schemas import RoomSchema, RoomCreateIn, RoomUpdateIn, RoomIdResponse, SuccessResponse, RoomListResponse, \
    RoomDetailResponse
from settings.auth import AuthBearer, auth_check, master_check
from utils.response import ErrorResponseSchema
from utils.error import server_error_return, not_found_error_return, error_codes, CtudyException

router = Router(tags=['Room'])
logger = logging.getLogger('room')


@router.get("/", response={200: RoomListResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@auth_check
def list_room(request):
    try:
        room_list = Room.objects.filter(
            Q(members=request.user) | Q(roomconfig__master=request.user),
            is_deleted=False
        )

        result = list()
        for room in room_list:
            result.append({
                **RoomSchema.validate(room).dict(),
                'member_count': room.members.count() + 1,
                'master_name': room.roomconfig.master.name
            })

        return_data = {
            'result': True,
            'response': result
        }
        return 200, return_data

    except Http404:
        return 404, not_found_error_return

    except CtudyException as e:
        return e.code, e.message

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.post("/", response={200: RoomIdResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@auth_check
def create_room(request, payload: RoomCreateIn, file: UploadedFile = None):
    try:
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

        return_data = {
            'result': True,
            'response': {
                "id": room.id
            }
        }
        return 200, return_data

    except CtudyException as e:
        return e.code, e.message

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.get("/{room_id}", response={200: RoomDetailResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@auth_check
def get_room(request, room_id: str):
    try:
        room = Room.objects.filter(id=room_id, is_deleted=False)

        if not room.exists():
            raise CtudyException(404, not_found_error_return)

        room = room[0]

        return_data = {
            'result': True,
            'response': {
                **RoomSchema.validate(room).dict(),
                'members': list(room.members.all()),
                'master': room.roomconfig.master
            }
        }
        return 200, return_data

    except Http404:
        return 404, not_found_error_return

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.put("/{room_id}", response={200: RoomIdResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@auth_check
@master_check
def update_room(request, room_id: str, payload: RoomUpdateIn):
    try:
        room = None
        for attr, value in payload.dict().items():
            if value is not None:
                if attr == 'master':
                    member = get_object_or_404(Member, id=value)
                    room = member.room_set.filter(id=room_id)
                    if room.exists():
                        room = room[0]
                        room.members.remove(member)
                        room.members.add(request.user)
                        room.roomconfig.master = member
                        room.roomconfig.save()
                else:
                    room = get_object_or_404(Room, id=room_id)
                    setattr(room, attr, value)
                    room.save()

        return_data = {
            'result': True,
            'response': {
                "id": room.id
            }
        }
        return 200, return_data

    except Http404:
        return 404, not_found_error_return

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.delete("/{room_id}", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@auth_check
@master_check
def delete_room(request, room_id: str):
    try:
        room = get_object_or_404(Room, id=room_id)
        room.is_deleted = True
        room.deleted_time = datetime.datetime.now()
        room.save()

        return_data = {
            'result': True,
            'response': {
                'success': True
            }
        }
        return 200, return_data

    except Http404:
        return 404, not_found_error_return

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return
