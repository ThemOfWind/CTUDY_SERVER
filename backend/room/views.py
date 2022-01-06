import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Member
from room.docs import RoomDoc
from room.models import Room, RoomConfig
from room.serializers import RoomSerializer, RoomConfigSerializer

logger = logging.getLogger('account')

server_error_return = {'result': False, 'response': {'message': 'Internal Server Error'}}
param_error_return = {'result': False, 'response': {'message': 'parameter is not present'}}
auth_error_return = {'result': False, 'response': {'message': 'AuthenticationException'}}
active_error_return = {'result': False, 'response': {'message': 'User is not activated'}}
exist_error_return = {'result': False, 'response': {'message': 'Username exists'}}
not_found_error_return = {'result': False, 'response': {'message': 'Not found data'}}
data_conflict_error_return = {'result': False, 'response': {'message': 'Data conflict error'}}


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

            member = Member.objects.filter(user=request.user)
            if not member.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST, data=param_error_return)
            member = member[0]

            if Room.objects.filter(name=name).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST, data=param_error_return)

            room = Room.objects.create(name=name)
            room.members.add(member)
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
