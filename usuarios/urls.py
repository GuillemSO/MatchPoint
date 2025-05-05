from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('home/', views.home_view, name='home'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path("home_admin_club/", views.home_admin_club, name="home_admin_club"),
]
