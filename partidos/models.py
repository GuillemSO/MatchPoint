from django.db import models
from estado_reserva.models import EstadoReserva
from pistas.models import Pista
from clubs.models import Club
from usuarios.models import Usuario
from resultados.models import Resultado

class Partido(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado_reserva = models.ForeignKey(EstadoReserva, on_delete=models.CASCADE)
    resultado_partido = models.ForeignKey(Resultado, on_delete=models.CASCADE, blank=True, null=True)
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Partido {self.id} - {self.fecha}"
