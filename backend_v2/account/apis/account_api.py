import datetime
import logging
import requests

from uuid import uuid4
from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import Router, Form, UploadedFile
from oauth2_provider.models import Application, RefreshToken, AccessToken

from account.models import Member, CertificateCode
from account.schemas import LoginSchema, SignupSchema, TokenResponse, ProfileResponse, \
    SignupSuccessResponse, FindIdSchema, FindPwSchema, CertificateSchema, ProfileNameSchema, \
    PasswordChangeSchema, UsernameCheckResponse, CertificateKeyResponse, ResetPwSchema
from settings.auth import AuthBearer, auth_check
from utils.base import base_api
from utils.gmail import send_message
from utils.response import ErrorResponseSchema, SuccessResponse
from utils.error import server_error_return, auth_error_return, error_codes, exist_error_return, CtudyException, \
    not_found_error_return, param_error_return

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


@router.get("/signup/", response={200: SuccessResponse, error_codes: ErrorResponseSchema})
@base_api(logger)
def username_email_check(request, username: str = None, email: str = None):
    if username is None and email is None:
        raise CtudyException(code=400, message=param_error_return)

    if username is not None:
        if Member.objects.filter(username=username).exists():
            raise CtudyException(code=400, message=exist_error_return)

    if email is not None:
        if Member.objects.filter(email=email).exists():
            raise CtudyException(code=400, message=exist_error_return)

    return {'success': True}


@router.post("/signup/", response={200: SignupSuccessResponse, error_codes: ErrorResponseSchema})
@base_api(logger)
def signup(request, payload: SignupSchema = Form(...), file: UploadedFile = None):
    payload_data = payload.dict()

    if Member.objects.filter(username=payload_data['username']).exists():
        raise CtudyException(code=400, message=exist_error_return)

    member = Member.objects.create_user(**payload_data)

    if file is not None:
        member.image = file
        member.save()

    return {'username': member.username, 'name': member.name}


@router.get("/logout/", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def logout(request):
    RefreshToken.objects.filter(user=request.user).delete()
    AccessToken.objects.filter(user=request.user).delete()
    return {'success': True}


@router.delete("/withdraw/", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def withdraw(request):
    request.user.delete()
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


@router.put("/profile/", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def update_profile(request, payload: ProfileNameSchema):
    for attr, value in payload.dict().items():
        if value is not None:
            setattr(request.user, attr, value)
            request.user.save()

    return {'success': True}


@router.post("/profile/", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def update_profile_image(request, file: UploadedFile = None):
    request.user.image = file
    request.user.save()

    return {'success': True}


@router.put("/password/", response={200: SuccessResponse, error_codes: ErrorResponseSchema}, auth=AuthBearer())
@base_api(logger)
@auth_check
def update_password(request, payload: PasswordChangeSchema):
    payload_data = payload.dict()
    if not request.user.check_password(payload_data['password']):
        raise CtudyException(401, auth_error_return)

    request.user.set_password(payload_data['new_password'])
    request.user.save()

    return {'success': True}


@router.post("/findid/", response={200: UsernameCheckResponse, error_codes: ErrorResponseSchema})
@base_api(logger)
def find_id(request, payload: FindIdSchema):
    payload_data = payload.dict()

    member = get_object_or_404(Member, email=payload_data['email'])

    return {'username': member.username}


@router.post("/findpw/", response={200: SuccessResponse, error_codes: ErrorResponseSchema})
@base_api(logger)
def find_pw(request, payload: FindPwSchema):
    payload_data = payload.dict()

    member = get_object_or_404(Member, username=payload_data['username'], email=payload_data['email'])

    # 인증번호 생성
    certificate = uuid4().hex.upper()
    certificate_code = certificate[:6]
    certificate_key = certificate[6:12]
    expire = datetime.datetime.now() + datetime.timedelta(minutes=3)
    CertificateCode.objects.create(member=member, code=certificate_code, key=certificate_key, expire=expire)

    # 메일 발송
    # send_message(to=payload_data['email'], subject='[Ctudy] 비밀번호 재설정 인증', code=certificate_code)
    send_message(to='pb1123love@gmail.com', subject='[Ctudy] 비밀번호 재설정 인증', code=certificate_code)

    return {'success': True}


@router.post("/findpw/certificate/", response={200: CertificateKeyResponse, error_codes: ErrorResponseSchema})
@base_api(logger)
def check_certificate_code(request, payload: CertificateSchema):
    payload_data = payload.dict()
    now = datetime.datetime.now()

    certificate = CertificateCode.objects.filter(member__username=payload_data['username'],
                                                 member__email=payload_data['email'],
                                                 code=payload_data['code'],
                                                 expire__gt=now)

    if not certificate.exists():
        raise CtudyException(code=404, message=not_found_error_return)

    certificate = certificate.first()
    certificate.is_checked = True
    certificate.save()

    return {'key': certificate.key}


@router.post("/findpw/reset/", response={200: SuccessResponse, error_codes: ErrorResponseSchema})
@base_api(logger)
def reset_pw(request, payload: ResetPwSchema):
    payload_data = payload.dict()

    certificate = CertificateCode.objects.filter(member__username=payload_data['username'],
                                                 member__email=payload_data['email'],
                                                 key=payload_data['key'],
                                                 is_checked=True)
    if not certificate.exists():
        raise CtudyException(code=404, message=not_found_error_return)

    member = certificate.first().member
    member.set_password(payload_data['new_password'])
    member.save()

    return {'success': True}
