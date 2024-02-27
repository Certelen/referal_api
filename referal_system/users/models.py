from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    referer = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='referer_user',
        verbose_name='Реферер',
        null=True,
        blank=True
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True
    )

    def __str__(self):
        return self.username
