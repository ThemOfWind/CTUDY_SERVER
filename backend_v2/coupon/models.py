import os
from uuid import uuid4

from django.db import models

from account.models import Member
from room.models import Room


def path_and_rename(instance, filename):
    upload_to = f'public/coupon/{instance.room.id}/'
    ext = filename.split('.')[-1]
    # ext = 'png'
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Coupon(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=path_and_rename, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sender', to_field='')
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='receiver')
    is_use = models.BooleanField(default=False)
    used_date = models.DateField(null=True)
    created_date = models.DateField(auto_created=True, auto_now_add=True)
