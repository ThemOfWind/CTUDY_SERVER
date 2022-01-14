import datetime
import logging

import requests
from django.conf import settings
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.models import Application, RefreshToken, AccessToken
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from account.docs import SignInDoc, SignUpDoc, LogoutDoc
from account.models import Member

logger = logging.getLogger('account')

server_error_return = {'result': False, 'error': {'message': 'Internal Server Error'}}
param_error_return = {'result': False, 'error': {'message': 'parameter is not present'}}
auth_error_return = {'result': False, 'error': {'message': 'AuthenticationException'}}
active_error_return = {'result': False, 'error': {'message': 'User is not activated'}}
exist_error_return = {'result': False, 'error': {'message': 'Username exists'}}
not_found_error_return = {'result': False, 'error': {'message': 'Not found data'}}
data_conflict_error_return = {'result': False, 'error': {'message': 'Data conflict error'}}


class SignInView(APIView):
    """
    SignInView: 로그인 API
    """

    @staticmethod
    @swagger_auto_schema(
        request_body=SignInDoc.post_data_type,
        responses={200: SignInDoc.post_success_resp}
    )
    def post(request):
        """
        post:
            # 로그인 API
        """
        try:
            if 'username' not in request.data or 'password' not in request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=param_error_return)
            username = request.data['username']
            password = request.data['password']

            user = User.objects.filter(username=username)
            if not user.exists():
                return Response(status=status.HTTP_401_UNAUTHORIZED, data=auth_error_return)
            user = user[0]
            if not user.check_password(password):
                return Response(status=status.HTTP_401_UNAUTHORIZED, data=auth_error_return)

            if not user.is_active:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=active_error_return)

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
                return Response(status=status.HTTP_401_UNAUTHORIZED, data=auth_error_return)

            return_data = {
                'result': True,
                'response': response.json()
            }

            return Response(status=status.HTTP_200_OK, data=return_data)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)


class SignUpView(APIView):
    """
    SignInView: 회원가입 API
    """

    @staticmethod
    @swagger_auto_schema(
        manual_parameters=[SignUpDoc.param_data_type],
        responses={200: SignUpDoc.success_resp}
    )
    def get(request):
        """
        get:
            # 아이디 중복 검사 API
        """
        try:
            username = request.query_params.get('username')

            if User.objects.filter(username=username).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST, data=exist_error_return)
            else:
                return_data = {
                    'result': True,
                    'response': {
                        'username': username
                    }
                }
                return Response(status=status.HTTP_200_OK, data=return_data)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)

    @staticmethod
    @swagger_auto_schema(
        request_body=SignUpDoc.post_data_type,
        responses={200: SignUpDoc.success_resp}
    )
    def post(request):
        """
        post:
            # 회원가입 API
        """
        try:
            if 'username' not in request.data or 'password' not in request.data or 'name' not in request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=param_error_return)

            username = request.data['username']
            password = request.data['password']
            name = request.data['name']

            if User.objects.filter(username=username).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST, data=exist_error_return)

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

            return Response(status=status.HTTP_200_OK, data=return_data)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)


class LogoutView(APIView):
    """
    LogoutView: 로그아웃 API
    """

    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @swagger_auto_schema(
        responses={200: LogoutDoc.post_success_resp}
    )
    def get(request):
        """
        get:
            # 로그아웃 API
        """
        try:
            refresh_token_list = RefreshToken.objects.filter(user=request.user)
            for refresh_token in refresh_token_list:
                refresh_token.revoked = datetime.datetime.now()
                refresh_token.save()

            AccessToken.objects.filter(user=request.user).delete()

            return_data = {
                'result': True,
                'response': None
            }

            return Response(status=status.HTTP_200_OK, data=return_data)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)
