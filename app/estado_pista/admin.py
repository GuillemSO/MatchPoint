from django.contrib import admin
from .models import EstadoPista

@admin.register(EstadoPista)
class EstadoPistaAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado')
    search_fields = ('estado',)
    ordering = ('estado',)
