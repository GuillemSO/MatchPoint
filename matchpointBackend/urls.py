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
from app.usuarios.views import UsuarioViewSet
from rest_framework import routers
from app.usuarios.views import UsuarioViewSet
from app.clubs.views import ClubViewSet
from app.estado_pista.views import EstadoPistaViewSet
from app.estado_reserva.views import EstadoReservaViewSet
from app.invitaciones.views import InvitacionesViewSet
from app.partidos.views import PartidoViewSet
from app.pistas.views import PistaViewSet
from app.resultados.views import ResultadoPartidoViewSet
from app.tipo_pista.views import TipoPistaViewSet
from app.tipo_usuario.views import TipoUsuarioViewSet
from app.usuarios.views import home_view
from django.urls import path, include
from app.usuarios.views import login_view, logout_view

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
    path('', login_view, name='home_redirect'), 
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('usuarios/', include('app.usuarios.urls')),
    path('clubs/', include('app.clubs.urls')),
    path('pistas/', include('app.pistas.urls')),
]

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
