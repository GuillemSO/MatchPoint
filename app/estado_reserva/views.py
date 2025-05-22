from rest_framework import viewsets
from .models import EstadoReserva
from .serializers import EstadoReservaSerializer

class EstadoReservaViewSet(viewsets.ModelViewSet):
    queryset = EstadoReserva.objects.all()
    serializer_class = EstadoReservaSerializer
