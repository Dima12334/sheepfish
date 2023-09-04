from django.contrib import admin
from django.urls import path, include

api_urlpatterns = [
    path('', include('apps.printers.api.urls')),
    path('', include('apps.checks.api.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
]
