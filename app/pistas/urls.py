from django.urls import path
from .views import PistaListView
from app.pistas import views as views

urlpatterns = [
    path('', PistaListView.as_view(), name='pista-list'),
    path('crear/', views.pista_create, name='pista-create'),
    path('<int:pk>/editar/', views.pista_update, name='pista-update'),
    path('<int:pk>/eliminar/', views.pista_delete, name='pista-delete'),
]
