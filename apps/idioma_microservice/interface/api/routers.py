from rest_framework.routers import DefaultRouter
from apps.idioma_microservice.interface.api.views import IdiomaViewSet

router = DefaultRouter()
router.register(r'idiomas', IdiomaViewSet, basename='idioma')

urlpatterns = router.urls
