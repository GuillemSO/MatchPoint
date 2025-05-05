from django.contrib import admin
from .models import Resultado

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'jugador_1', 'jugador_2', 'jugador_3', 'jugador_4', 'resultado_1', 'resultado_2')
    search_fields = ('jugador_1__nombre', 'jugador_2__nombre', 'jugador_3__nombre', 'jugador_4__nombre')
    list_filter = ('resultado_1', 'resultado_2')
    ordering = ('id',)
