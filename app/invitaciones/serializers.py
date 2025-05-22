from rest_framework import serializers
from .models import Invitaciones

class InvitacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitaciones
        fields = '__all__'
        read_only_fields = ['usuario', 'estado']

    def create(self, validated_data):
        validated_data['estado'] = 'pendiente'
        return super().create(validated_data)