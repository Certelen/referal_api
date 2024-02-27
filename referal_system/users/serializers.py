from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import User
from .validate import validate_code, validate_email, validate_username


class PostUserCreateSerializer(UserCreateSerializer):
    referal_code = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'referal_code',
            'email',
            'username',
            'password'
        )

    def validate(self, data):
        validate_email(data.get('email'))
        validate_username(data.get('username'))
        if data.get('referal_code'):
            validate_code(data.get('referal_code'))
        return data

    def save(self, **kwargs):
        if 'referal_code' in self.validated_data:
            self.validated_data.pop('referal_code')
        super(PostUserCreateSerializer, self).save(**kwargs)


class GetUserSerializer(UserSerializer):
    referer_user = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'referer_user',
        )
