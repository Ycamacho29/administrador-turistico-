from rest_framework.routers import DefaultRouter
from apps.paquete_turistico_microservice.interface.api.views import PaqueteTuristicoViewSet

router = DefaultRouter()
router.register(r'paquetes-turisticos', PaqueteTuristicoViewSet, basename='paquete-turistico')

urlpatterns = router.urls
