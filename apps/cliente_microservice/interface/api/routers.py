from rest_framework.routers import DefaultRouter
from apps.cliente_microservice.interface.api.views import ClienteViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')

urlpatterns = router.urls
