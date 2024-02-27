import datetime as dt

from django.core.mail import EmailMessage
from django.http import JsonResponse
from rest_framework import response, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticated

from referal_system.settings import EMAIL_HOST_USER

from .models import Referal
from .serializers import ReferalSerializer


class ReferalViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Referal.objects.all()
    serializer_class = ReferalSerializer

    def list(self, request, *args, **kwargs):
        user_referal = Referal.objects.filter(code_owner=request.user)
        if user_referal:
            user_referal = user_referal[0]
        serializer = self.get_serializer(user_referal)
        return response.Response(serializer.data)

    def perform_create(self, serializer, data={}):
        user = self.request.user
        search_exist = Referal.objects.filter(code_owner=user)
        data['created_date'] = dt.date.today()
        if search_exist:
            if search_exist.filter(end_date__gte=data['created_date']):
                raise serializers.ValidationError(
                    'Ваш реферальный код уже существует:'
                    f'{search_exist[0].code}'
                )
        data['code_owner'] = user
        data['id'] = user.id
        data['code'] = Referal.create_code()
        data['validity_period'] = int(
            serializer.validated_data.get('validity_period')
        )
        data['end_date'] = Referal.get_end_date(
            data['created_date'], data['validity_period']
        )
        return serializer.save(**data)

    def delete(self, request, *args, **kwargs):
        instance = Referal.objects.filter(code_owner=request.user)
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def get_referal_on_mail(self, request):
        current_user = request.user
        if not current_user.email:
            raise serializers.ValidationError(
                'Не указана почта')
        HEAD_TEXT = 'Реферальный код'
        text = f"Ваш реферальный код: {current_user.ref_owner.code}"
        email = EmailMessage(
            HEAD_TEXT,
            text,
            to=[current_user.email,],
            from_email=EMAIL_HOST_USER
        )
        email.send()
        return response.Response(
            JsonResponse({'result': 'Реферальный код отправлен на почту'}),
            status=status.HTTP_201_CREATED
        )
