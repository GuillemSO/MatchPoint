from django.contrib import admin
from .models import EstadoReserva

@admin.register(EstadoReserva)
class EstadoReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado')
    search_fields = ('estado',)
    ordering = ('estado',)
