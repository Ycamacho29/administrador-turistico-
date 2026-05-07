from rest_framework.routers import DefaultRouter
from apps.tipo_paquete_microservice.interface.api.views import TipoPaqueteViewSet

router = DefaultRouter()
router.register(r'tipos-paquetes', TipoPaqueteViewSet, basename='tipo-paquete')

urlpatterns = router.urls
