from django.db import models

from account.models import Member
from room.models import Room


class Coupon(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sender', to_field='')
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='receiver')
    is_use = models.BooleanField(default=False)
    used_date = models.DateField(null=True)
