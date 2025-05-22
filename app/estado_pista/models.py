from django.db import models

class EstadoPista(models.Model):
    estado = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.estado
