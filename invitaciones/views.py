from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Invitaciones
from .serializers import InvitacionesSerializer

class InvitacionesViewSet(viewsets.ModelViewSet):
    queryset = Invitaciones.objects.all()
    serializer_class = InvitacionesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['estado']

    def get_queryset(self):
        # Solo devuelve las invitaciones creadas por el usuario autenticado
        return Invitaciones.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Asigna el usuario automáticamente al crear
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def recordatorio(self, request, pk=None):
        invitacion = self.get_object()

        if invitacion.estado != 'pendiente':
            return Response({'detail': 'Solo puedes enviar recordatorios a invitaciones pendientes.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Aquí podrías agregar lógica de reenvío de email (opcional)
        return Response({'detail': f'Recordatorio enviado a {invitacion.invitado_email}'})
