from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', include('djoser.urls.jwt')),
    path('', include('api.urls')),

]
