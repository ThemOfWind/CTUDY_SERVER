import datetime
import logging
from typing import List

from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router

from room.models import Room
from room.schemas import PostSuccess, ErrorMessage, RoomSchemaIn, RoomSchema, SuccessStatus
from utils.common import AuthBearer
from utils.error import server_error_return, not_found_error_return


router = Router(tags=['Room'])
logger = logging.getLogger('room')


@router.get("/", response={200: List[RoomSchema], 404: ErrorMessage, 500: ErrorMessage}, auth=AuthBearer())
def get_room(request):
    try:
        return 200, Room.objects.all()

    except Http404:
        return 404, not_found_error_return

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.post("/", response={200: PostSuccess, 500: ErrorMessage})
def create_room(request, payload: RoomSchemaIn):
    try:
        room = Room.objects.create(**payload.dict())
        return 200, {"id": room.id}
    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.get("/{room_id}", response={200: RoomSchema, 404: ErrorMessage, 500: ErrorMessage})
def get_room(request, room_id: str):
    try:
        room = get_object_or_404(Room, id=room_id, is_deleted=False)
        return 200, room

    except Http404:
        return 404, not_found_error_return

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.put("/{room_id}", response={200: PostSuccess, 404: ErrorMessage, 500: ErrorMessage})
def update_room(request, room_id: str, payload: RoomSchemaIn):
    try:
        room = get_object_or_404(Room, id=room_id)
        for attr, value in payload.dict().items():
            setattr(room, attr, value)
        room.save()
        return 200, {"id": room.id}

    except Http404:
        return 404, not_found_error_return

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.delete("/{room_id}", response={200: SuccessStatus, 404: ErrorMessage, 500: ErrorMessage})
def delete_room(request, room_id: str):
    try:
        room = get_object_or_404(Room, id=room_id)
        room.is_deleted = True
        room.deleted_time = datetime.datetime.now()
        room.save()
        return 200, {"success": True}

    except Http404:
        return 404, not_found_error_return

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return
