import os
from uuid import uuid4

from django.db import models

from account.models import Member


def path_and_rename(instance, filename):
    upload_to = 'public/room/'
    ext = filename.split('.')[-1]
    # ext = 'png'
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Room(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(Member)
    banner = models.ImageField(upload_to=path_and_rename, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(null=True)


class RoomConfig(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    master = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
