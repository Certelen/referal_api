from rest_framework import serializers

from referals.models import Referal

from .models import User


def validate_email(email: str) -> None:
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError(
            'Пользователь с этой почтой уже существует.'
        )


def validate_username(username: str) -> None:
    if username == 'me':
        raise serializers.ValidationError(
            'Нельзя использовать "me" как имя.'
        )
    if User.objects.filter(username=username).exists():
        raise serializers.ValidationError(
            'Пользователь с этим именем уже существует.'
        )


def validate_code(code: str) -> None:
    if (code and
            not Referal.objects.filter(code=code).exists()):
        raise serializers.ValidationError(
            'Недействительный реферальный код.'
        )
