import datetime
import logging

from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router, Form, UploadedFile

from account.models import Member
from room.models import Room, RoomConfig
from room.schemas import RoomSchema, RoomCreateIn, RoomUpdateIn, RoomIdResponse, SuccessResponse, RoomListResponse, \
    RoomDetailResponse, MemberSchema
from settings.auth import AuthBearer, auth_check, master_check
from utils.response import ErrorResponseSchema
from utils.error import server_error_return, not_found_error_return, error_codes, CtudyException

router = Router(tags=['Room'])
logger = logging.getLogger('room')


@router.get("/", response={200: RoomListResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@auth_check
def list_room(request):
    try:
        room_list = Room.objects.filter(members__user=request.user, is_deleted=False)\
            .prefetch_related('roomconfig_set')\
            .prefetch_related('members')

        result = list()
        for room in room_list:
            room_data = {
                **RoomSchema.validate(room).dict(),
                'member_count': room.members.count(),
                'master_name': room.roomconfig_set.get(room=room).master.name
            }
            result.append(room_data)
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
def create_room(request, payload: RoomCreateIn = Form(...), file: UploadedFile = None):
    try:
        payload_data = payload.dict()
        if file is not None:
            payload_data['banner'] = file
        room = Room.objects.create(**payload_data)
        room.members.add(request.user)
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
        room = Room.objects.filter(id=room_id, is_deleted=False)\
            .prefetch_related('roomconfig_set') \
            .prefetch_related('members')

        if not room.exists():
            raise CtudyException(404, not_found_error_return)

        room = room[0]

        return_data = {
            'result': True,
            'response': {
                **RoomSchema.validate(room).dict(),
                'members': [MemberSchema.validate(m) for m in room.members.all()],
                'master': room.roomconfig_set.get(room=room).master
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
        room = get_object_or_404(Room, id=room_id)
        for attr, value in payload.dict().items():
            if value is not None:
                if attr == 'master':
                    room_config = get_object_or_404(RoomConfig, room=room)
                    room_config.master = get_object_or_404(Member, id=value)
                    room_config.save()
                else:
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
