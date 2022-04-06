import logging
import sys

from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Member
from account.serializers import MemberListSerializer
from ctudy_server.pagination import CustomPagination
from room.docs import RoomDoc, MemberListDoc
from room.models import Room, RoomConfig
from room.serializers import RoomSerializer, RoomConfigSerializer

logger = logging.getLogger('room')

server_error_return = {'result': False, 'error': {'message': 'Internal Server Error'}}
param_error_return = {'result': False, 'error': {'message': 'parameter is not present'}}
auth_error_return = {'result': False, 'error': {'message': 'AuthenticationException'}}
active_error_return = {'result': False, 'error': {'message': 'User is not activated'}}
exist_error_return = {'result': False, 'error': {'message': 'Username exists'}}
not_found_error_return = {'result': False, 'error': {'message': 'Not found data'}}
data_conflict_error_return = {'result': False, 'error': {'message': 'Data conflict error'}}


class RoomView(APIView):
    """
    RoomView: 스터디 룸 API
    """

    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @swagger_auto_schema(
        responses={200: RoomDoc.list_success_resp}
    )
    def get(request):
        """
        get:
            # 전체 스터디 룸 조회 API
        """
        try:
            room_queryset = Room.objects.filter(members__user=request.user)
            rooms = RoomSerializer(room_queryset, many=True).data
            for room in rooms:
                room['member_count'] = len(room['members'])
                room.pop('members')

                room_config_queryset = RoomConfig.objects.filter(room__id=room['id'])
                if not room_config_queryset.exists():
                    return Response(status=status.HTTP_404_NOT_FOUND, data=not_found_error_return)

                room['master_name'] = room_config_queryset[0].master.name

            return_data = {
                'result': True,
                'response': rooms
            }

            return Response(status=status.HTTP_200_OK, data=return_data)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)

    @staticmethod
    @swagger_auto_schema(
        request_body=RoomDoc.post_data_type,
        responses={200: RoomDoc.post_success_resp}
    )
    def post(request):
        """
        post:
            # 스터디 룸 등록 API
        """
        try:
            if 'name' not in request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=param_error_return)

            name = request.data['name']
            member_list = request.data.get('member_list')

            member = Member.objects.filter(user=request.user)
            if not member.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST, data=param_error_return)
            member = member[0]

            if Room.objects.filter(name=name).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST, data=param_error_return)

            room = Room.objects.create(name=name)
            room.members.add(member)

            if member_list is not None:
                member_list = [get_object_or_404(Member, pk=m) for m in member_list]
                if len(member_list) > 0:
                    room.members.add(*member_list)

            room.save()
            RoomConfig.objects.create(room=room, master=member)

            return_data = {
                'result': True,
                'response': None
            }
            return Response(status=status.HTTP_200_OK, data=return_data)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)


class SingleRoomView(APIView):
    """
    SingleRoomView: 개별 스터디 룸 API
    """

    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @swagger_auto_schema(
        responses={200: RoomDoc.success_resp}
    )
    def get(request, pk):
        """
        get:
            # 개별 스터디 룸 조회 API
        """
        try:
            room_queryset = Room.objects.filter(members__user=request.user, pk=pk)
            if not room_queryset.exists():
                return Response(status=status.HTTP_404_NOT_FOUND, data=not_found_error_return)

            room_config_queryset = RoomConfig.objects.filter(room=room_queryset[0])
            if not room_config_queryset.exists():
                return Response(status=status.HTTP_404_NOT_FOUND, data=not_found_error_return)

            room_config = RoomConfigSerializer(room_config_queryset[0]).data
            room = RoomSerializer(room_queryset[0]).data

            delete_member = None
            for member in room['members']:
                if member['id'] == room_config['master']['id']:
                    delete_member = member
                    break

            room['members'].remove(delete_member)

            return_data = {
                'result': True,
                'response': {
                    **room,
                    **room_config
                }
            }

            return Response(status=status.HTTP_200_OK, data=return_data)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)

    @staticmethod
    @swagger_auto_schema(
        request_body=RoomDoc.put_data_type,
        responses={200: RoomDoc.post_success_resp}
    )
    def put(request, pk):
        """
        put:
            # 개별 스터디 룸 수정 API
        """
        try:
            name = request.data.get('name')
            master = request.data.get('master')

            room_queryset = Room.objects.filter(members__user=request.user, pk=pk)
            if not room_queryset.exists():
                return Response(status=status.HTTP_404_NOT_FOUND, data=not_found_error_return)
            room = room_queryset[0]

            if name is not None:
                room.name = name
                room.save()

            if master is not None:
                member = Member.objects.filter(pk=master)
                if not member.exists():
                    return Response(status=status.HTTP_404_NOT_FOUND, data=not_found_error_return)
                member = member[0]

                room_config = RoomConfig.objects.filter(room=room)
                if not room_config.exists():
                    return Response(status=status.HTTP_404_NOT_FOUND, data=not_found_error_return)
                room_config = room_config[0]

                room_config.master = member
                room_config.save()

            return_data = {
                'result': True,
                'response': None
            }
            return Response(status=status.HTTP_200_OK, data=return_data)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)

    @staticmethod
    @swagger_auto_schema(
        responses={200: RoomDoc.post_success_resp}
    )
    def delete(request, pk):
        """
        delete:
            # 개별 스터디 룸 삭제 API
        """
        try:
            room_queryset = Room.objects.filter(members__user=request.user, pk=pk)
            if not room_queryset.exists():
                return Response(status=status.HTTP_404_NOT_FOUND, data=not_found_error_return)
            room_queryset.delete()

            return_data = {
                'result': True,
                'response': None
            }
            return Response(status=status.HTTP_200_OK, data=return_data)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)


class MemberListView(generics.ListAPIView):
    """
    MemberListView: 전체 회원 리스트 API
    get:
        # 전체 회원 리스트 조회 API
    """

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = MemberListSerializer

    @staticmethod
    def get_return_data(member_list):
        """
        :param member_list: 쿼리 결과 직렬화 데이터
        """
        try:
            for member in member_list:
                user = member.pop('user')
                member['username'] = user['username']

            return_dict = {
                'result': True,
                'response': {
                    'list': member_list
                }
            }
            return return_dict

        except Exception as e:
            _a, _b, tb = sys.exc_info()
            logger.error(f'except line: {tb.tb_lineno}, message: {e.__str__()}')
            return None

    @staticmethod
    def set_filters(order_field, order):
        """
        :param order_field: 정렬 규칙
        :param order: 정렬할 컬럼
        """
        try:
            member_queryset = Member.objects.all().order_by(f'{order}{order_field}').distinct()

            return member_queryset

        except Exception as e:
            logger.error(e)
            return 500, 0

    def list(self, request, *args, **kwargs):
        """
        Django List API Form
        """
        try:
            max_page = request.query_params.get('max_page')
            if max_page is not None:
                self.paginator.page_size = int(max_page)
            else:
                self.paginator.page_size = 10

            order_field = request.query_params.get('order_field')
            if order_field is None:
                order_field = 'name'

            order = request.query_params.get('order')

            if str(order) == 'asc':
                order = ''
            elif str(order) == 'desc':
                order = '-'
            else:
                order = '-'

            queryset = self.set_filters(order_field, order)
            if queryset == 500 or None:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)
            elif queryset == 400:
                return Response(status=status.HTTP_200_OK, data={
                    'result': True,
                    'response': []
                })

            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return_data = self.get_return_data(serializer.data)
                if return_data is None:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)

                return self.get_paginated_response(return_data)

            serializer = self.get_serializer(queryset, many=True)
            return_data = self.get_return_data(serializer.data)
            if return_data is None:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)

            return Response(return_data)

        except NotFound as e:
            logger.error(e)
            return Response(status=status.HTTP_404_NOT_FOUND, data=not_found_error_return)
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)

    @swagger_auto_schema(
        manual_parameters=[
            MemberListDoc.param_max_page_data,
            MemberListDoc.param_order_data,
            MemberListDoc.param_order_field_data
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RoomMemberView(APIView):
    """
    RoomMemberView: 스터디 룸 멤버 API
    """

    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @swagger_auto_schema(
        request_body=RoomDoc.post_member_data_type,
        responses={200: RoomDoc.post_success_resp}
    )
    def post(request, pk):
        """
        post:
            # 스터디 룸 멤버 등록 API
        """
        try:
            room = get_object_or_404(Room, pk=pk)
            room_config = get_object_or_404(RoomConfig, room=room)

            if request.user != room_config.master.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data=auth_error_return)

            member_list = request.data.get('member_list')
            member_list = [get_object_or_404(Member, pk=m) for m in member_list]

            if len(member_list) > 0:
                room.members.add(*member_list)
                room.save()

            return_data = {
                'result': True,
                'response': None
            }
            return Response(status=status.HTTP_200_OK, data=return_data)

        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND, data=not_found_error_return)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)

    @staticmethod
    @swagger_auto_schema(
        request_body=RoomDoc.post_member_data_type,
        responses={200: RoomDoc.post_success_resp}
    )
    def delete(request, pk):
        """
        delete:
            # 스터디 룸 멤버 삭제 API
        """
        try:
            room = get_object_or_404(Room, pk=pk)
            room_config = get_object_or_404(RoomConfig, room=room)

            if request.user != room_config.master.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data=auth_error_return)

            member_list = request.data.get('member_list')
            [room.members.remove(get_object_or_404(Member, pk=m)) for m in member_list if m != room_config.master.pk]

            return_data = {
                'result': True,
                'response': None
            }
            return Response(status=status.HTTP_200_OK, data=return_data)

        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND, data=not_found_error_return)

        except Exception as e:
            logger.error(e.__str__())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=server_error_return)
