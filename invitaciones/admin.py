from django.contrib import admin
from .models import Invitaciones

@admin.register(Invitaciones)
class InvitacionesAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'invitado_email', 'partido')
    search_fields = ('usuario__nombre', 'invitado_email', 'partido__id')
    list_filter = ('partido', 'usuario')
    ordering = ('-id',)
