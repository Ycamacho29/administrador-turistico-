from rest_framework.routers import DefaultRouter
from apps.destino_turistico_microservice.interface.api.views import DestinoTuristicoViewSet

router = DefaultRouter()
router.register(r'destinos-turisticos', DestinoTuristicoViewSet, basename='destino-turistico')

urlpatterns = router.urls
