from django.db import models
from tipo_usuario.models import TipoUsuario

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    nivel_padel = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    foto_perfil_url = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre
