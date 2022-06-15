import os
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


def path_and_rename(instance, filename):
    upload_to = 'public/profile/'
    ext = filename.split('.')[-1]
    # ext = 'png'
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Member(AbstractUser):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to=path_and_rename, blank=True, null=True)
    first_name = None
    last_name = None


class CertificateCode(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    key = models.CharField(max_length=6)
    is_checked = models.BooleanField(default=False)
    expire = models.DateTimeField()
