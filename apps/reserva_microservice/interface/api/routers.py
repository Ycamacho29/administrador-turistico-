from rest_framework.routers import DefaultRouter
from apps.reserva_microservice.interface.api.views import ReservaViewSet

router = DefaultRouter()
router.register(r'reservas', ReservaViewSet, basename='reserva')

urlpatterns = router.urls
