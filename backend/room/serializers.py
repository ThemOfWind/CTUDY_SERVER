from rest_framework.serializers import ModelSerializer

from account.serializers import MemberSerializer
from room.models import RoomConfig, Room


class RoomConfigSerializer(ModelSerializer):
    master = MemberSerializer(read_only=True)

    class Meta:
        model = RoomConfig
        fields = ('master',)


class RoomSerializer(ModelSerializer):
    members = MemberSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = ('id',
                  'name',
                  'members')
