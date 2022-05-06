from functools import wraps

from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja.security import HttpBearer
from oauth2_provider.models import AccessToken

from room.models import Room
from utils.error import auth_error_return, not_found_error_return, CtudyException


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            access_token = get_object_or_404(AccessToken, token=token)
            import datetime
            if token == access_token.token and datetime.datetime.now() < access_token.expires:
                request.user = access_token.user
                return token
        except Http404:
            raise CtudyException(401, auth_error_return)


def auth_check(ori_func):
    @wraps(ori_func)
    def inner(request, **kwargs):
        if type(request.auth) is not str and not request.auth[-1]:
            raise CtudyException(401, auth_error_return)
        return ori_func(request, **kwargs)
    return inner


def master_check(ori_func):
    @wraps(ori_func)
    def inner(request, **kwargs):
        room = Room.objects.filter(id=kwargs['room_id'])
        if not room.exists():
            raise CtudyException(404, not_found_error_return)
        room = room[0]
        if request.user != room.roomconfig.master:
            raise CtudyException(401, auth_error_return)
        return ori_func(request, **kwargs)
    return inner
