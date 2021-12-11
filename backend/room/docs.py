from drf_yasg import openapi


class RoomDoc:
    # Request
    id_field = openapi.Schema(
        'id',
        description='member id',
        type=openapi.TYPE_INTEGER
    )
    request_name_field = openapi.Schema(
        'name',
        description='스터디 룸 이름',
        type=openapi.TYPE_STRING
    )
    post_data_type = openapi.Schema(
        'data',
        description='POST Data Body',
        type=openapi.TYPE_OBJECT,
        properties={
            'name': request_name_field,
        }
    )

    put_data_type = openapi.Schema(
        'data',
        description='PUT Data Body',
        type=openapi.TYPE_OBJECT,
        properties={
            'name': request_name_field,
            'master': id_field
        }
    )

    # Response
    member_data = openapi.Schema(
        'member data',
        type=openapi.TYPE_OBJECT,
        properties={
            'id': id_field,
            'name': request_name_field,
        }
    )

    success_resp_data = openapi.Schema(
        'response data',
        type=openapi.TYPE_OBJECT,
        properties={
            'name': request_name_field,
            'members': member_data,
            'master': member_data
        }
    )
    list_success_resp_data = openapi.Schema(
        'response data (list)',
        type=openapi.TYPE_OBJECT,
        properties={
            'id': id_field,
            'name': request_name_field
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
            'response': success_resp_data
        }
    )
    list_success_resp = openapi.Schema(
        'response',
        type=openapi.TYPE_OBJECT,
        properties={
            'result': result_field,
            'response': list_success_resp_data
        }
    )
    post_success_resp = openapi.Schema(
        'response',
        type=openapi.TYPE_OBJECT,
        properties={
            'result': result_field,
            'response': None
        }
    )
