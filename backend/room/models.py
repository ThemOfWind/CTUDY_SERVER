from django.db import models

from account.models import Member


class Room(models.Model):
    name = models.CharField(max_length=50)
    master = models.ForeignKey(Member, on_delete=models.SET_NULL)
    members = models.ManyToManyField(Member)
