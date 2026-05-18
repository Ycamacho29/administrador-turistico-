from rest_framework.routers import DefaultRouter
from apps.paqueteTuristico_servicio_microservice.interface.api.views import PaqueteturisticoServicioViewSet

router = DefaultRouter()
router.register(r'paquetesTuristicos-servicios', PaqueteturisticoServicioViewSet, basename='paqueteTuristico-servicio')

urlpatterns = router.urls
