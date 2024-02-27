from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', include('djoser.urls.jwt')),
    path('user/', include('users.urls')),
    path('referal/', include('referals.urls')),
    path('redoc/',
         TemplateView.as_view(template_name='redoc.html'),
         name='redoc'),
]
