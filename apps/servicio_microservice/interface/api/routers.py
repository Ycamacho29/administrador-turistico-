from rest_framework.routers import DefaultRouter
from apps.servicio_microservice.interface.api.views import ServicioViewSet

router = DefaultRouter()
router.register(r'servicios', ServicioViewSet, basename='servicio')

urlpatterns = router.urls
