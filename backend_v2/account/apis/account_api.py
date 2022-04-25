import logging

import requests
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router, Form, UploadedFile
from oauth2_provider.models import Application, RefreshToken, AccessToken

from account.models import Member
from account.schemas import LoginSchema, SignupSchema, SuccessStatusResponse, TokenResponse
from settings.auth import AuthBearer, auth_check
from utils.response import ErrorResponseSchema
from utils.error import server_error_return, param_error_return, auth_error_return, \
    error_codes, exist_error_return, CtudyException, not_found_error_return

router = Router(tags=['Account'])
logger = logging.getLogger('account')


@router.post("/signin/", response={200: TokenResponse, error_codes: ErrorResponseSchema})
def login(request, payload: LoginSchema):
    try:
        payload_data = payload.dict()
        if 'username' not in payload_data or 'password' not in payload_data:
            raise CtudyException(code=400, message=param_error_return)

        username = payload_data['username']
        password = payload_data['password']

        try:
            user = get_object_or_404(Member, username=username)
        except Http404:
            raise CtudyException(code=404, message=not_found_error_return)
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
        response = requests.post(url=settings.TOKEN_URL, data=url_data, headers=headers)
        if response.status_code != 200:
            raise CtudyException(401, auth_error_return)

        return_data = {
            'result': True,
            'response': response.json()
        }

        return 200, return_data

    except CtudyException as e:
        return e.code, e.message

    except Exception as e:
        logger.error(e.__str__())
        return 500, server_error_return


@router.post("/signup/", response={200: SuccessStatusResponse, error_codes: ErrorResponseSchema})
def signup(request, payload: SignupSchema = Form(...), file: UploadedFile = None):
    try:
        payload_data = payload.dict()

        if Member.objects.filter(username=payload_data['username']).exists():
            raise CtudyException(code=400, message=exist_error_return)

        member = Member.objects.create_user(username=payload_data['username'],
                                            password=payload_data['password'],
                                            email=payload_data['email'])

        if file is not None:
            member.image = file
            member.save()

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


@router.get("/logout/", response={200: SuccessStatusResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@auth_check
def logout(request):
    try:
        if type(request.auth) is not str and not request.auth[-1]:
            raise CtudyException(code=401, message=auth_error_return)

        RefreshToken.objects.filter(user=request.user).delete()
        AccessToken.objects.filter(user=request.user).delete()
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
