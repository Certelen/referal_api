from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    referal_code = models.CharField(
        'Реферальная ссылка',
        max_length=200,
        null=True
    )
