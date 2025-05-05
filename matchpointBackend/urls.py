"""
URL configuration for matchpointBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework import routers
from usuarios.views import UsuarioViewSet
from rest_framework import routers
from usuarios.views import UsuarioViewSet
from clubs.views import ClubViewSet
from estado_pista.views import EstadoPistaViewSet
from estado_reserva.views import EstadoReservaViewSet
from invitaciones.views import InvitacionesViewSet
from partidos.views import PartidoViewSet
from pistas.views import PistaViewSet
from resultados.views import ResultadoPartidoViewSet
from tipo_pista.views import TipoPistaViewSet
from tipo_usuario.views import TipoUsuarioViewSet
from usuarios.views import home_view

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'clubs', ClubViewSet)
router.register(r'estado_pista', EstadoPistaViewSet)
router.register(r'estado_reserva', EstadoReservaViewSet)
router.register(r'invitaciones', InvitacionesViewSet)
router.register(r'partidos', PartidoViewSet)
router.register(r'pistas', PistaViewSet)
router.register(r'resultados', ResultadoPartidoViewSet)
router.register(r'tipo_pista', TipoPistaViewSet)
router.register(r'tipo_usuario', TipoUsuarioViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('manager/clubs/', include('clubs.urls')),
    path('', include('usuarios.urls')),
    path('pistas/', include('pistas.urls')),
]

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
