from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.seguridad_microservice.interface.api.views import RoleViewSet, PermissionViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'permisos', PermissionViewSet, basename='permisos')

urlpatterns = router.urls
