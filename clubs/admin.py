from django.contrib import admin
from .models import Club

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion', 'telefono', 'email_contacto', 'usuario')
    search_fields = ('nombre', 'direccion', 'telefono', 'email_contacto', 'usuario__nombre')
    list_filter = ('usuario',)
    ordering = ('nombre',)
