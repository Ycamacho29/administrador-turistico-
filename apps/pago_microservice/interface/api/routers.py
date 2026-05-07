from rest_framework.routers import DefaultRouter
from apps.pago_microservice.interface.api.views import PagoViewSet

router = DefaultRouter()
router.register(r'pagos', PagoViewSet, basename='pago')

urlpatterns = router.urls
