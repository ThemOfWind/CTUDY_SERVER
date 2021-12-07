from django.db import models

from account.models import Member


class Room(models.Model):
    name = models.CharField(max_length=50),
    members = models.ManyToManyField(Member)
