from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from .models import Member


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class MemberSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = ('id',
                  'name')


class ProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ('id',
                  'user',
                  'name')
