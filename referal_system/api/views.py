from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin
)
from djoser.views import UserViewSet

import string
import random
import datetime as dt

from .models import Referal
from .serializers import PostReferalSerializer, GetUserSerializer


class ReferalViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Referal.objects.all()
    serializer_class = PostReferalSerializer

    def list(self, request, *args, **kwargs):
        user_referal = Referal.objects.filter(
            referal_owner=request.user)
        if user_referal:
            user_referal = user_referal[0]
        serializer = self.get_serializer(user_referal)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        created_date = dt.date.today()
        search_exist = Referal.objects.filter(
            referal_owner=user)
        while True:
            code = ''.join([random.choice(string.hexdigits)
                            for _ in range(21)])
            if Referal.objects.filter(code=code):
                continue
            break
        validity_period = int(serializer.validated_data.get('validity_period'))
        referal_enddate = created_date + dt.timedelta(
            days=validity_period
        )
        data = {
            'id': user.id,
            'code': code,
            'created_date': created_date,
            'validity_period': validity_period,
            'end_date': referal_enddate,
            'referal_owner': user
        }
        if search_exist:
            if search_exist.filter(
                end_date__gte=created_date
            ):
                raise serializers.ValidationError(
                    f'Реферальный код уже существует: {search_exist[0].code}'
                )
        return serializer.save(**data)

    def delete(self, request, *args, **kwargs):
        instance = Referal.objects.filter(
            referal_owner=request.user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(UserViewSet):

    def perform_create(self, serializer):
        """
        Запрос регистрации нового пользователя.
        Создаёт нового пользователя,
        если он не был создан ранее администратором.
        """
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        referal_code = serializer.validated_data.get('referal_code')
        data = {'username': username, 'email': email}
        if referal_code:
            data['referer'] = Referal.objects.get(
                code=referal_code).referal_owner
        serializer.save(**data)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GetUserSerializer(instance)
        return Response(serializer.data)
