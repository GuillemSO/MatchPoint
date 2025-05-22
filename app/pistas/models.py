from django.db import models
from app.estado_pista.models import EstadoPista
from app.tipo_pista.models import TipoPista
from app.clubs.models import Club

class Pista(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.FloatField()
    estado_pista = models.ForeignKey(EstadoPista, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    tipo_pista = models.ForeignKey(TipoPista, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
