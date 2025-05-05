from django.db import models

class TipoPista(models.Model):
    doble = models.BooleanField()
    individual = models.BooleanField()

    def __str__(self):
        return f"Doble: {self.doble}, Individual: {self.individual}"
