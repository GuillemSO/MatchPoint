from rest_framework import serializers
from .models import TipoPista

class TipoPistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPista
        fields = '__all__'
