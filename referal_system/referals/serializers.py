from rest_framework import serializers

from .models import Referal


class ReferalSerializer(serializers.ModelSerializer):
    validity_period = serializers.IntegerField(
        required=True,
        write_only=True,
        error_messages={
            'required':
            'Введите количество дней действия реферального кода'
        }
    )
    code = serializers.CharField(required=False)
    end_date = serializers.DateField(required=False)

    class Meta:
        fields = (
            'validity_period',
            'code',
            'end_date'
        )
        read_only = (
            'id',
        )
        model = Referal

    def validate(self, data):
        if 1 > data.get('validity_period') > 365:
            raise serializers.ValidationError(
                'Срок действия кода не меньше 1 дня и не больше 1 года'
            )
        return data
