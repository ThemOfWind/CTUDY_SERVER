import logging

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router, UploadedFile

from account.models import Member
from room.models import Room
from room.schemas import SuccessResponse, MemberJoinIn
from settings.auth import AuthBearer, auth_check, master_check
from utils.response import ErrorResponseSchema
from utils.error import server_error_return, not_found_error_return, error_codes, CtudyException

router = Router(tags=['Study - Member'])
logger = logging.getLogger('member')


@router.get("/", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@auth_check
def list_member(request):
    try:
        return_data = {
            'result': True,
            'response': True
        }
        return 200, return_data

    except Http404:
        return 404, not_found_error_return

    except CtudyException as e:
        return e.code, e.message

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.post("/{room_id}", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@auth_check
@master_check
def join_member(request, room_id: str, payload: MemberJoinIn):
    try:
        payload_data = payload.dict()
        room = get_object_or_404(Room, id=room_id)
        q = Q()
        [q.add(Q(id=member_id), Q.OR) for member_id in payload_data['member_list']]
        member_list = Member.objects.filter(q)
        room.members.add(*member_list)
        room.save()

        return_data = {
            'result': True,
            'response': {
                'success': True
            }
        }
        return 200, return_data

    except CtudyException as e:
        return e.code, e.message

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.delete("/{room_id}", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@auth_check
@master_check
def delete_member(request, room_id: str):
    try:

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
