from rest_framework.routers import DefaultRouter
from apps.estatus_pago_microservice.interface.api.views import EstatusPagoViewSet

router = DefaultRouter()
router.register(r'estatus-pagos', EstatusPagoViewSet, basename='estatus-pago')

urlpatterns = router.urls
