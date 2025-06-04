from django.urls import path
from . import views

urlpatterns = [
    path('', views.club_list_manager, name='club-list'),  # Aquí debe estar 'club-list'
    path('manager/list/', views.club_list_manager, name='club-list-manager'),
    path('admin/list/', views.club_list_admin, name='club-list-admin'),
    path('detail/<int:pk>/', views.club_detail, name='club-detail'),
    path('create/', views.club_create, name='club-create'),
    path('update/<int:pk>/', views.club_update, name='club-update'),
    path('delete/<int:pk>/', views.club_delete, name='club-delete'),
]