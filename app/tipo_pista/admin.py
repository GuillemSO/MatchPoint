from django.contrib import admin
from .models import TipoPista

@admin.register(TipoPista)
class TipoPistaAdmin(admin.ModelAdmin):
    list_display = ('id', 'doble', 'individual')
    list_filter = ('doble', 'individual')
    ordering = ('id',)
