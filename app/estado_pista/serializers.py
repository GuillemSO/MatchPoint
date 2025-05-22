from rest_framework import serializers
from .models import EstadoPista

class EstadoPistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPista
        fields = '__all__'
