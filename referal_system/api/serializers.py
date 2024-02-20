from rest_framework import serializers
from .models import Referal


class PostReferalSerializer(serializers.ModelSerializer):
    validity_period = serializers.IntegerField(
        required=True,
        write_only=True,
        error_messages={
            'required':
            'Введите количество дней действия реферального кода'
        }
    )

    class Meta:
        fields = (
            'validity_period',
        )
        read_only_field = (
            'code',
            'referal_code',
        )
        model = Referal


class GetReferalSerializer(serializers.Serializer):
    class Meta:
        fields = (
            'created_data',
            'code',
            'end_life',
        )
        model = Referal
