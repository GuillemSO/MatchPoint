from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('admin-club/', views.home_admin_club, name='home_admin_club'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # CRUD Usuarios (solo managers)
    path('list/', views.usuario_list, name='usuario-list'),
    path('detail/<int:pk>/', views.usuario_detail, name='usuario-detail'),
    path('create/', views.usuario_create, name='usuario-create'),
    path('update/<int:pk>/', views.usuario_update, name='usuario-update'),
    path('delete/<int:pk>/', views.usuario_delete, name='usuario-delete'),

    # Dashboard jugador
    path('jugador/', views.home_jugador, name='home_jugador'),
    
    # Gestión de invitaciones
    path('invitacion/aceptar/<int:invitacion_id>/', views.aceptar_invitacion, name='aceptar_invitacion'),
    path('invitacion/rechazar/<int:invitacion_id>/', views.rechazar_invitacion, name='rechazar_invitacion'),
    path('invitacion/crear/', views.crear_invitacion, name='crear_invitacion'),
    
    # Partidos
    path('mis-partidos/', views.mis_partidos, name='mis_partidos'),
    path('partido/<int:partido_id>/', views.detalle_partido, name='detalle_partido'),

    path('obtener-pistas-club/<int:club_id>/', views.obtener_pistas_club, name='obtener_pistas_club'),
    path('crear-partido/', views.crear_partido, name='crear_partido'),
]
