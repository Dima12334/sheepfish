from rest_framework.routers import DefaultRouter

from .views import CheckViewSet

app_name = 'checks'

router = DefaultRouter()
router.register('checks', CheckViewSet, basename='checks')
urlpatterns = router.urls
