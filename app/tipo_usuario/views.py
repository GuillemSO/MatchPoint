from rest_framework import viewsets
from .models import TipoUsuario
from .serializers import TipoUsuarioSerializer

class TipoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = TipoUsuario.objects.all()
    serializer_class = TipoUsuarioSerializer
