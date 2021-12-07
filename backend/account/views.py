import logging

from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from knox.models import AuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.docs import SignInDoc

logger = logging.getLogger('account')

server_error_return = {'result': False, 'response': {'message': 'Internal Server Error'}}
param_error_return = {'result': False, 'response': {'message': 'parameter is not present'}}
auth_error_return = {'result': False, 'response': {'message': 'AuthenticationException'}}
active_error_return = {'result': False, 'response': {'message': 'User is not activated'}}
exist_error_return = {'result': False, 'response': {'message': 'Username exists'}}
not_found_error_return = {'result': False, 'response': {'message': 'Not found data'}}
data_conflict_error_return = {'result': False, 'response': {'message': 'Data conflict error'}}


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

            instance, token = AuthToken.objects.create(user)
            return_data = {
                "result": True,
                "response": {
                    'access_token': token
                }
            }
            return Response(data=return_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)
