from django.db import models
from app.usuarios.models import Usuario

class Club(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email_contacto = models.CharField(max_length=150)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('club-detail', kwargs={'pk': self.pk})