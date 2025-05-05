from django.db import models
from usuarios.models import Usuario
from partidos.models import Partido


ESTADOS_INVITACION = (
    ('pendiente', 'Pendiente'),
    ('aceptada', 'Aceptada'),
    ('rechazada', 'Rechazada'),
)

class Invitaciones(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="invitaciones_enviadas")
    invitado_email = models.EmailField()
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS_INVITACION, default='pendiente')

    def __str__(self):
        return f"Invitación de {self.usuario.email} a {self.invitado_email}"