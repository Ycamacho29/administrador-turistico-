from rest_framework.routers import DefaultRouter
from apps.pais_microservice.interface.api.views import PaisViewSet

router = DefaultRouter()
router.register(r'paises', PaisViewSet, basename='pais')

urlpatterns = router.urls
