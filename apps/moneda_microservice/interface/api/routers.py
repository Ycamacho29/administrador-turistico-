from rest_framework.routers import DefaultRouter
from apps.moneda_microservice.interface.api.views import MonedaViewSet

router = DefaultRouter()
router.register(r'monedas', MonedaViewSet, basename='moneda')

urlpatterns = router.urls
