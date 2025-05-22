from rest_framework import viewsets
from .models import Resultado
from .serializers import ResultadoPartidoSerializer

class ResultadoPartidoViewSet(viewsets.ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoPartidoSerializer
