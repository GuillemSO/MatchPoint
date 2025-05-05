from rest_framework import serializers
from .models import Pista

class PistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pista
        fields = '__all__'
