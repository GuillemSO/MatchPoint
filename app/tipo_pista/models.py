from django.db import models

class TipoPista(models.Model):
    doble = models.BooleanField()
    individual = models.BooleanField()

    def __str__(self):
        return f"Doble: {self.doble}, Individual: {self.individual}"

    def save(self, *args, **kwargs):
        if self.doble == self.individual:
            raise ValueError("TipoPista debe ser doble o individual, no ambos ni ninguno.")
        super().save(*args, **kwargs)
