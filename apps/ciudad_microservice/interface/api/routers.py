from rest_framework.routers import DefaultRouter
from apps.ciudad_microservice.interface.api.views import CiudadViewSet

router = DefaultRouter()
router.register(r'ciudades', CiudadViewSet, basename='ciudad')

urlpatterns = router.urls
