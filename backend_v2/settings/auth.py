from functools import wraps

from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja.security import HttpBearer
from oauth2_provider.models import AccessToken

from room.models import Room
from utils.error import auth_error_return


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            access_token = get_object_or_404(AccessToken, token=token)
            import datetime
            if token == access_token.token and datetime.datetime.now() < access_token.expires:
                request.user = access_token.user
                return token
        except Http404:
            return 401, False


def auth_check(ori_func):
    @wraps(ori_func)
    def inner(request, **kwargs):
        if type(request.auth) is not str and not request.auth[-1]:
            return 401, auth_error_return
        return ori_func(request, **kwargs)
    return inner


def master_check(ori_func):
    @wraps(ori_func)
    def inner(request, **kwargs):
        room = Room.objects.filter(id=kwargs['room_id'])[0]
        if request.user != room.roomconfig.master:
            return 401, auth_error_return
        return ori_func(request, **kwargs)
    return inner
