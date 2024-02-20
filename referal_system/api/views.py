from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
import datetime as dt
import uuid
import base64

from .models import Referal
from .serializers import PostReferalSerializer, GetReferalSerializer


class ReferalViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Referal.objects.all()
    serializer_class = PostReferalSerializer

    def perform_create(self, serializer):
        code = base64.standard_b64encode(
            uuid.uuid1().bytes.rstrip())
        created_data = dt.datetime.now()
        referal_endlife = created_data + dt.timedelta(
            days=int(serializer.validated_data.get('validity_period'))
        )
        return serializer.save(
            code=code,
            created_data=created_data,
            end_life=referal_endlife
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = GetReferalSerializer(instance)
        return Response(instance_serializer.data)
