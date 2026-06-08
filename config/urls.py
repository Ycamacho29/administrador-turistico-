"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.ciudad_microservice.interface.api.routers')),
    path('api/', include('apps.pais_microservice.interface.api.routers')),
    path('api/', include('apps.idioma_microservice.interface.api.routers')),
    path('api/', include('apps.moneda_microservice.interface.api.routers')),
    path('api/', include('apps.servicio_microservice.interface.api.routers')),
    path('api/', include('apps.tipo_paquete_microservice.interface.api.routers')),
    path('api/', include('apps.estatus_reserva_microservice.interface.api.routers')),
    path('api/', include('apps.estatus_pago_microservice.interface.api.routers')),
    path('api/', include('apps.metodo_pago_microservice.interface.api.routers')),
    path('api/', include('apps.pago_microservice.interface.api.routers')),
    path('api/', include('apps.destino_turistico_microservice.interface.api.routers')),
    path('api/', include('apps.paquete_turistico_microservice.interface.api.routers')),
    path('api/', include('apps.cliente_microservice.interface.api.routers')),
    path('api/', include('apps.reserva_microservice.interface.api.routers')),
    path('api/', include('apps.paqueteTuristico_servicio_microservice.interface.api.routers')),
    path('api/', include('apps.authentication_microservice.interface.api.routers')),
    path('api/', include('apps.seguridad_microservice.interface.api.routers')),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
