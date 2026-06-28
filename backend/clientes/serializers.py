from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Cliente
        fields = '__all__'

    def validate(self, data):
        """Ejecuta full_clean del modelo y convierte ValidationError de DRF"""
        # Crear instancia temporal para validar
        if self.instance:
            # Update: usar instancia existente con datos nuevos
            for attr, value in data.items():
                setattr(self.instance, attr, value)
            instance = self.instance
        else:
            # Create: crear nueva instancia
            instance = Cliente(**data)
        
        try:
            instance.full_clean()
        except ValidationError as e:
            # Convertir a error de serializer (lo maneja DRF como 400)
            raise serializers.ValidationError(e.message_dict)
        
        return data