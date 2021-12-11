from django.db import models

from account.models import Member


class Room(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(Member)


class RoomConfig(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    master = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
