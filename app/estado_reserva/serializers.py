from rest_framework import serializers
from .models import EstadoReserva

class EstadoReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoReserva
        fields = '__all__'
