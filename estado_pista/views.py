from rest_framework import viewsets
from .models import EstadoPista
from .serializers import EstadoPistaSerializer

class EstadoPistaViewSet(viewsets.ModelViewSet):
    queryset = EstadoPista.objects.all()
    serializer_class = EstadoPistaSerializer
