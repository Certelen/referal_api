from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import Referal, User


class PostReferalSerializer(serializers.ModelSerializer):
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


class PostUserCreateSerializer(UserCreateSerializer):
    referal_code = serializers.CharField(required=False)

    class Meta:
        fields = (
            'referal_code',
            'email',
            'username',
            'password'
        )
        model = User

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        referal_code = data.get('referal_code')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с этой почтой уже существует.'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с этим именем уже существует.'
            )
        if (referal_code and
                not Referal.objects.filter(code=referal_code).exists()):
            raise serializers.ValidationError(
                'Недействительный реферальный код.'
            )
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" как имя.'
            )
        return data

    def save(self, **kwargs):
        if 'referal_code' in self.validated_data:
            self.validated_data.pop('referal_code')
        super(PostUserCreateSerializer, self).save(**kwargs)


class GetUserSerializer(UserSerializer):
    referer_user = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    class Meta:
        fields = (
            'id',
            'email',
            'username',
            'referer_user',
        )
        model = User
