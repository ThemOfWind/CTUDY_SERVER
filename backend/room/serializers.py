from rest_framework.serializers import ModelSerializer

from account.serializers import ProfileSerializer
from room.models import RoomConfig, Room


class RoomConfigSerializer(ModelSerializer):
    master = ProfileSerializer(read_only=True)

    class Meta:
        model = RoomConfig
        fields = ('master',)


class RoomSerializer(ModelSerializer):
    members = ProfileSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = ('id',
                  'name',
                  'members')
