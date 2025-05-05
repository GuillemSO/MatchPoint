from rest_framework import viewsets
from .models import TipoPista
from .serializers import TipoPistaSerializer

class TipoPistaViewSet(viewsets.ModelViewSet):
    queryset = TipoPista.objects.all()
    serializer_class = TipoPistaSerializer
