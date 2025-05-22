from django.contrib import admin
from .models import Partido

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'hora_inicio', 'hora_fin', 'estado_reserva', 'pista', 'club', 'usuario', 'resultado_partido')
    search_fields = ('club__nombre', 'pista__nombre', 'usuario__nombre')
    list_filter = ('fecha', 'estado_reserva', 'club', 'pista')
    ordering = ('-fecha', 'hora_inicio')
