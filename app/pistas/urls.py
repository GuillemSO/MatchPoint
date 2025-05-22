from django.urls import path
from .views import PistaListView
from .views import crear_pista
urlpatterns = [
    path('', PistaListView.as_view(), name='pista-list'),
    path('crear/', crear_pista, name='pista-create'),
]
