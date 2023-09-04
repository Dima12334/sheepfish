from rest_framework.routers import DefaultRouter

from .views import PrinterViewSet

app_name = 'printers'

router = DefaultRouter()
router.register('printers', PrinterViewSet, basename='printers')
urlpatterns = router.urls
