from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReferalViewSet

app_name = 'api'

router_v1 = DefaultRouter()
# router_v1.register('users', UserViewSet, basename='users')
router_v1.register('referal', ReferalViewSet, basename='referals')

urlpatterns = [
    path('', include(router_v1.urls)),
]
