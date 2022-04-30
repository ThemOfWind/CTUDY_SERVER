import logging

import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import Router, Form, UploadedFile
from oauth2_provider.models import Application, RefreshToken, AccessToken

from account.models import Member
from account.schemas import LoginSchema, SignupSchema, TokenResponse, ProfileResponse, \
    UsernameCheckResponse
from settings.auth import AuthBearer, auth_check
from utils.base import base_api
from utils.response import ErrorResponseSchema, SuccessResponse
from utils.error import server_error_return, auth_error_return, error_codes, exist_error_return, CtudyException

router = Router(tags=['Account'])
logger = logging.getLogger('account')


@router.post("/signin/", response={200: TokenResponse, error_codes: ErrorResponseSchema})
@base_api(logger)
def login(request, payload: LoginSchema):
    payload_data = payload.dict()
    username = payload_data['username']
    password = payload_data['password']

    user = get_object_or_404(Member, username=username)

    if not user.check_password(password) or not user.is_active:
        raise CtudyException(code=401, message=auth_error_return)

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
    try:
        response = requests.post(url=settings.TOKEN_URL, data=url_data, headers=headers)
    except Exception as e:
        raise CtudyException(500, e.__str__())
    if response.status_code != 200:
        raise CtudyException(401, auth_error_return)

    return response.json()


@router.get("/signup/", response={200: UsernameCheckResponse, error_codes: ErrorResponseSchema})
@base_api(logger)
def username_check(request, username: str):
    if Member.objects.filter(username=username).exists():
        raise CtudyException(code=400, message=exist_error_return)

    return {'username': username}


@router.post("/signup/", response={200: SuccessResponse, error_codes: ErrorResponseSchema})
@base_api(logger)
def signup(request, payload: SignupSchema = Form(...), file: UploadedFile = None):
    payload_data = payload.dict()

    if Member.objects.filter(username=payload_data['username']).exists():
        raise CtudyException(code=400, message=exist_error_return)

    member = Member.objects.create_user(**payload_data)

    if file is not None:
        member.image = file
        member.save()

    return {'success': True}


@router.get("/logout/", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def logout(request):
    RefreshToken.objects.filter(user=request.user).delete()
    AccessToken.objects.filter(user=request.user).delete()
    return {'success': True}


@router.get("/profile/", response={200: ProfileResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def profile(request):
    try:
        return request.user

    except CtudyException as e:
        return e.code, e.message

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return
