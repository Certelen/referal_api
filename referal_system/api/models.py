from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta
import random
import string

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    referer = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='referer_user',
        verbose_name='Реферер',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username


class Referal(models.Model):
    referal_owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='ref_owner',
        verbose_name='Владелец кода',
    )
    code = models.CharField(
        'Реферальный код',
        max_length=200,
        blank=True
    )
    created_date = models.DateField(
        'Дата создания кода',
        db_index=True,
    )
    validity_period = models.PositiveSmallIntegerField(
        'Срок действия кода',
        validators=(MinValueValidator(1),
                    MaxValueValidator(365))
    )
    end_date = models.DateField(
        'Окончание работы кода',
        db_index=True,
        blank=True
    )

    def clean(self):
        self.end_date = self.created_date + timedelta(
            days=self.validity_period
        )
        if not self.code:
            while True:
                code = ''.join([random.choice(string.hexdigits)
                                for _ in range(21)])
                if Referal.objects.filter(code=code):
                    continue
                self.code = code
                break
        else:
            if Referal.objects.filter(code=self.code):
                return "Такой код уже существует!"
