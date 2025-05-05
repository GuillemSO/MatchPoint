from django.db import models
from usuarios.models import Usuario

class Resultado(models.Model):
    jugador_1 = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True , related_name="jugador_1")
    jugador_2 = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True , related_name="jugador_2")
    jugador_3 = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True , related_name="jugador_3", blank=True)
    jugador_4 = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True , related_name="jugador_4", blank=True)
    resultado_1 = models.IntegerField()
    resultado_2 = models.IntegerField()

    def __str__(self):
        return f"Resultado {self.id}"
