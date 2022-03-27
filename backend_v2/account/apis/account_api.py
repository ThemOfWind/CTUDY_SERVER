import logging

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router
from oauth2_provider.models import Application

from account.models import Member
from account.schemas import PostSuccess, ErrorMessage, ResponseSchema, LoginSchema, SignupSchema
from utils.common import AuthBearer
from utils.error_messages import server_error_return, not_found_error_return, param_error_return, auth_error_return, \
    error_codes, exist_error_return

router = Router(tags=['Account'])
logger = logging.getLogger('account')


@router.post("/signin/", response={200: ResponseSchema, error_codes: ErrorMessage})
def login(request, payload: LoginSchema):
    try:
        payload_data = payload.dict()
        if 'username' not in payload_data or 'password' not in payload_data:
            return 400, param_error_return

        username = payload_data['username']
        password = payload_data['password']

        user = get_object_or_404(User, username=username)
        if not user.check_password(password) or not user.is_active:
            return 401, auth_error_return

        app_objects = Application.objects.filter(name=settings.APP_NAME)
        if not app_objects.exists():
            app = Application.objects.create(authorization_grant_type='password',
                                             client_type='confidential',
                                             name=settings.APP_NAME)
        else:
            app = app_objects[0]

        url_data = {
            'client_id': app.client_id,
            'client_secret': app.client_secret,
            'grant_type': app.authorization_grant_type,
            'username': username,
            'password': password
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url=settings.TOKEN_URL, data=url_data, headers=headers)
        if response.status_code != 200:
            return 401, auth_error_return

        return_data = {
            'result': True,
            'response': response.json()
        }

        return 200, return_data
    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.post("/signup/", response={200: ResponseSchema, error_codes: ErrorMessage})
def signup(request, payload: SignupSchema):
    try:
        payload_data = payload.dict()
        if 'username' not in payload_data or 'password' not in payload_data or 'name' not in payload_data:
            return 400, param_error_return

        username = payload_data['username']
        password = payload_data['password']
        name = payload_data['name']

        if User.objects.filter(username=username).exists():
            return 400, exist_error_return

        user = User.objects.create_user(username=username,
                                        email=username,
                                        password=password)
        Member.objects.create(user=user,
                              name=name)

        return_data = {
            'result': True,
            'response': {
                'username': username,
                'name': name
            }
        }

        return 200, return_data
    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


# @router.get("/{account_id}", response={200: RoomSchema, 404: ErrorMessage, 500: ErrorMessage})
# def logout(request, account_id: str):
#     try:
#         account = get_object_or_404(Room, id=account_id, is_deleted=False)
#         return 200, account
#
#     except Http404:
#         return 404, not_found_error_return
#
#     except Exception as e:
#         logger.error(e.__str__())
#         return 500, server_error_return
