from drf_yasg import openapi


class RoomDoc:
    # Request
    id_field = openapi.Schema(
        'id',
        description='room id',
        type=openapi.TYPE_INTEGER
    )
    request_name_field = openapi.Schema(
        'name',
        description='스터디 룸 이름',
        type=openapi.TYPE_STRING
    )
    member_count_field = openapi.Schema(
        'member_count',
        description='스터디 룸 인원 수',
        type=openapi.TYPE_INTEGER
    )
    master_name_field = openapi.Schema(
        'master_name',
        description='스터디 룸 방장 이름',
        type=openapi.TYPE_STRING
    )
    member_pk_field = openapi.Schema(
        'pk',
        description='멤버 pk',
        type=openapi.TYPE_INTEGER
    )
    member_list_field = openapi.Schema(
        'member_list',
        description='멤버 pk 리스트',
        type=openapi.TYPE_ARRAY,
        items=member_pk_field
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

    post_member_data_type = openapi.Schema(
        'data',
        description='POST Data Body',
        type=openapi.TYPE_OBJECT,
        properties={
            'member_list': member_list_field
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
            'name': request_name_field,
            'member_count': member_count_field,
            'master_name': master_name_field
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


class MemberListDoc:
    # Request
    param_max_page_data = openapi.Parameter(
        'max_page',
        openapi.IN_QUERY,
        description='리턴 시 최대 개수',
        type=openapi.TYPE_INTEGER
    )
    param_order_field_data = openapi.Parameter(
        'order_field',
        openapi.IN_QUERY,
        description='정렬할 필드',
        type=openapi.TYPE_STRING
    )
    param_order_data = openapi.Parameter(
        'order',
        openapi.IN_QUERY,
        description='정렬 규칙 (asc, desc)',
        type=openapi.TYPE_STRING
    )
