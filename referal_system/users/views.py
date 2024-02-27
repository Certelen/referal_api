from djoser.views import UserViewSet
from rest_framework.response import Response

from referals.models import Referal

from .serializers import GetUserSerializer


class UserViewSet(UserViewSet):

    def perform_create(self, serializer, data={}):
        data['email'] = serializer.validated_data.get('email')
        data['username'] = serializer.validated_data.get('username')
        referal_code = serializer.validated_data.get('referal_code')
        if referal_code:
            data['referer'] = Referal.objects.get(
                code=referal_code
            ).code_owner
        serializer.save(**data)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GetUserSerializer(instance)
        return Response(serializer.data)
