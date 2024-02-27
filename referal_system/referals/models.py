import random
import string
from datetime import date, timedelta

from asgiref.sync import sync_to_async
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class AsyncManager(models.Manager):

    @sync_to_async
    def create_async(self, **kwargs):
        return self.create(**kwargs)


class Referal(models.Model):
    code_owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='Владелец кода',
    )
    code = models.CharField(
        'Реферальный код',
        max_length=200,
        unique=True,
        null=True,
        blank=True
    )
    created_date = models.DateField(
        'Дата создания кода',
        db_index=True,
        auto_now=True
    )
    validity_period = models.PositiveSmallIntegerField(
        'Срок действия кода',
        validators=(MinValueValidator(1),
                    MaxValueValidator(365))
    )
    end_date = models.DateField(
        'Окончание работы кода',
        null=True,
        blank=True
    )
    objects = AsyncManager()

    class Meta:
        verbose_name = 'Реферальный код'
        verbose_name_plural = 'Реферальные коды'
        ordering = ('created_date',)

    @sync_to_async
    def save_async(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def clean(self):
        self.end_date = self.get_end_date(
            self.created_date if self.created_date else date.today(),
            self.validity_period
        )
        if not self.code:
            self.code = self.create_code()
        super().clean()

    @staticmethod
    def get_end_date(now_date, validity_period):
        return now_date + timedelta(days=validity_period)

    @staticmethod
    def create_code():
        while True:
            code = ''.join([random.choice(string.hexdigits)
                            for _ in range(21)])
            if Referal.objects.filter(code=code):
                continue
            break
        return code

    def __str__(self):
        return (f'Код {self.code} пользователя {self.code_owner} '
                f'действителен до {self.end_date}')
