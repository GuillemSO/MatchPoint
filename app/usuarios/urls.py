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
]
