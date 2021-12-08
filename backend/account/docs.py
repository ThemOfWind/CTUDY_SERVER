from drf_yasg import openapi


class SignInDoc:
    # Response
    access_token_field = openapi.Schema(
        'access_token',
        description='access token',
        type=openapi.TYPE_STRING
    )
    expires_in_field = openapi.Schema(
        'expires_in',
        description='토큰 유효기간',
        type=openapi.TYPE_INTEGER
    )
    token_type_field = openapi.Schema(
        'token_type',
        description='token type (Bearer)',
        type=openapi.TYPE_STRING
    )
    scope_field = openapi.Schema(
        'scope',
        description='권한 범위',
        type=openapi.TYPE_STRING
    )
    refresh_token_field = openapi.Schema(
        'refresh_token',
        description='refresh token',
        type=openapi.TYPE_STRING
    )
    post_response_resp = openapi.Schema(
        'response',
        type=openapi.TYPE_OBJECT,
        properties={
            'access_token': access_token_field,
            'expires_in': expires_in_field,
            'token_type': token_type_field,
            'scope': scope_field,
            'refresh_token': refresh_token_field
        }
    )
    result_field = openapi.Schema(
        'result',
        description='처리 결과',
        type=openapi.TYPE_BOOLEAN
    )
    post_success_resp = openapi.Schema(
        'response',
        type=openapi.TYPE_OBJECT,
        properties={
            'result': result_field,
            'response': post_response_resp
        }
    )

    # Request
    request_username_field = openapi.Schema(
        'username',
        description='username (email)',
        type=openapi.TYPE_STRING
    )
    request_password_field = openapi.Schema(
        'password',
        description='password',
        type=openapi.TYPE_STRING
    )
    post_data_type = openapi.Schema(
        'data',
        description='POST Data Body',
        type=openapi.TYPE_OBJECT,
        properties={
            'username': request_username_field,
            'password': request_password_field,
        }
    )


class SignUpDoc:
    # Response
    username_field = openapi.Schema(
        'username',
        description='username (email)',
        type=openapi.TYPE_STRING
    )
    response_resp = openapi.Schema(
        'response',
        type=openapi.TYPE_OBJECT,
        properties={
            'username': username_field
        }
    )
    result_field = openapi.Schema(
        'result',
        description='처리 결과',
        type=openapi.TYPE_BOOLEAN
    )
    success_resp = openapi.Schema(
        'response',
        type=openapi.TYPE_OBJECT,
        properties={
            'result': result_field,
            'response': response_resp
        }
    )

    # Request
    param_data_type = openapi.Parameter(
        'username',
        openapi.IN_QUERY,
        description='username (email)',
        type=openapi.TYPE_STRING
    )
    request_username_field = openapi.Schema(
        'username',
        description='username (email)',
        type=openapi.TYPE_STRING
    )
    request_password_field = openapi.Schema(
        'password',
        description='password',
        type=openapi.TYPE_STRING
    )
    request_name_field = openapi.Schema(
        'name',
        description='name',
        type=openapi.TYPE_STRING
    )
    request_doctor_code_field = openapi.Schema(
        'doctor_code',
        description='doctor_code',
        type=openapi.TYPE_STRING
    )
    request_birthday_field = openapi.Schema(
        'birthday',
        description='birthday',
        type=openapi.TYPE_STRING
    )
    request_gender_field = openapi.Schema(
        'gender',
        description='gender',
        type=openapi.TYPE_STRING
    )
    request_phone_field = openapi.Schema(
        'phone',
        description='phone',
        type=openapi.TYPE_STRING
    )
    post_data_type = openapi.Schema(
        'data',
        description='POST Data Body',
        type=openapi.TYPE_OBJECT,
        properties={
            'username': request_username_field,
            'password': request_password_field,
            'name': request_name_field,
            'doctor_code': request_doctor_code_field,
            'birthday': request_birthday_field,
            'gender': request_gender_field,
            'phone': request_phone_field
        }
    )


class LogoutDoc:
    # Response
    result_field = openapi.Schema(
        'result',
        description='처리 결과',
        type=openapi.TYPE_BOOLEAN
    )
    post_success_resp = openapi.Schema(
        'response',
        type=openapi.TYPE_OBJECT,
        properties={
            'result': result_field,
            'response': None
        }
    )
