import datetime
import os
from typing import Any
from uuid import uuid4

from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Schema
from ninja.security import HttpBearer
from oauth2_provider.models import AccessToken

from utils.error import auth_error_return


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            access_token = get_object_or_404(AccessToken, token=token)
            if token == access_token.token and datetime.datetime.now() < access_token.expires:
                request.user = access_token.user
                return token
        except Http404:
            return 401, False


def path_and_rename(instance, filename):
    upload_to = 'public/profile/'
    ext = filename.split('.')[-1]
    # ext = 'png'
    filename = '{}.{}'.format(uuid4().hex, ext)

    return os.path.join(upload_to, filename)


class ResponseSchema(Schema):
    result: bool
    response: Any


class ErrorMessage(Schema):
    message: str


class ErrorResponseSchema(Schema):
    result: bool = False
    error: ErrorMessage
