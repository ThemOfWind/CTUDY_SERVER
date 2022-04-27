from rest_framework.serializers import ModelSerializer

from .models import Member


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = ('id',
                  'username',
                  'name')
