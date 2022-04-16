from django.contrib.auth.models import User
from django.db import models

from utils.common import path_and_rename


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to=path_and_rename, blank=True, null=True)
