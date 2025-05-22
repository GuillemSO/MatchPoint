from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuario_list, name='usuario-list'),
    path('crear/', views.usuario_create, name='usuario-create'),
    path('<int:pk>/', views.usuario_detail, name='usuario-detail'),
    path('<int:pk>/editar/', views.usuario_update, name='usuario-update'),
    path('<int:pk>/eliminar/', views.usuario_delete, name='usuario-delete'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('admin/', views.home_admin_club, name='home_admin_club'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('home/', views.home_view, name='home'),
]
