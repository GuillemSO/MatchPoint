from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'nivel_padel', 'fecha_registro', 'tipo_usuario')
    search_fields = ('nombre', 'email')
    list_filter = ('tipo_usuario', 'fecha_registro')
    ordering = ('-fecha_registro',)  # Ordenar por fecha de registro de forma descendente
