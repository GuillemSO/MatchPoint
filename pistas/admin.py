from django.contrib import admin
from .models import Pista

@admin.register(Pista)
class PistaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'estado_pista', 'club', 'tipo_pista')
    search_fields = ('nombre', 'club__nombre')
    list_filter = ('estado_pista', 'tipo_pista', 'club')
    ordering = ('nombre',)
