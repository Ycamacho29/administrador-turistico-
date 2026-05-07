from rest_framework.routers import DefaultRouter
from apps.metodo_pago_microservice.interface.api.views import MotodoPagoViewSet

router = DefaultRouter()
router.register(r'metodos-pago', MotodoPagoViewSet, basename='metodo-pago')

urlpatterns = router.urls
