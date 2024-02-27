from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ReferalViewSet

app_name = 'referals'

router_v1 = SimpleRouter()
router_v1.register('', ReferalViewSet, basename='referals')

urlpatterns = [
    path('', include(router_v1.urls)),
]
