from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Referals(models.Model):
    code = models.CharField(
        'Реферальная ссылка',
        max_length=200,
    )
    created_data = models.DateTimeField(
        'Дата создания ссылки',
        auto_now_add=True,
        db_index=True,
    )
    validity_period = models.PositiveSmallIntegerField(
        'Срок действия ссылки',
        validators=(MinValueValidator(1),
                    MaxValueValidator(365)),
    )

    class Meta:
        ordering = ('-created_data', )
