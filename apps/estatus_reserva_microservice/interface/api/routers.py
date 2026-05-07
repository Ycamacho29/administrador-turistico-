from rest_framework.routers import DefaultRouter
from apps.estatus_reserva_microservice.interface.api.views import EstatusReservaViewSet

router = DefaultRouter()
router.register(r'estatus-reservas', EstatusReservaViewSet, basename='estatus-reserva')

urlpatterns = router.urls
