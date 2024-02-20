from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta


from django.contrib.auth.models import AbstractUser


class Referal(models.Model):
    code = models.CharField(
        'Реферальный код',
        max_length=200,
    )
    created_data = models.DateField(
        'Дата создания кода',
        db_index=True,
    )
    validity_period = models.PositiveSmallIntegerField(
        'Срок действия кода',
        validators=(MinValueValidator(1),
                    MaxValueValidator(365)),
        null=True
    )
    end_life = models.DateField(
        'Окончание работы кода',
        db_index=True,
    )

    class Meta:
        ordering = ('-created_data', )

    def clean(self):
        self.end_life = self.created_data + timedelta(
            days=self.validity_period
        )


class User(AbstractUser):
    referal_code = models.OneToOneField(
        'Referal',
        on_delete=models.CASCADE,
        related_name='referal',
        verbose_name='Реферальный код',
        null=True
    )
