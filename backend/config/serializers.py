"""
Serializer base con validación automática del modelo.
HEREDAR ESTE SERIALIZER en lugar de serializers.ModelSerializer
para obtener validaciones automáticas del modelo.
"""
from django.core.exceptions import ValidationError
from rest_framework import serializers


class ValidatedModelSerializer(serializers.ModelSerializer):
    """
    Serializer que ejecuta full_clean() del modelo durante la validación.
    
    Uso:
        class MiSerializer(ValidatedModelSerializer):
            class Meta:
                model = MiModel
                fields = '__all__'
    
    Las validaciones definidas en el modelo (clean(), clean_fields(), etc.)
    se ejecutarán automáticamente y los errores se devolverán como errores
    de serializer (HTTP 400) en lugar de errores de servidor (HTTP 500).
    """
    
    def validate(self, data):
        """
        Ejecuta full_clean() del modelo para validaciones adicionales.
        """
        # Construir instancia para validar
        if self.instance:
            # Update: usar instancia existente con datos nuevos
            for attr, value in data.items():
                setattr(self.instance, attr, value)
            instance = self.instance
        else:
            # Create: crear nueva instancia con los datos entrantes
            instance = self.Meta.model(**data)
        
        # Ejecutar validaciones del modelo (clean(), clean_fields(), etc.)
        try:
            instance.full_clean()
        except ValidationError as e:
            # Convertir ValidationError de Django a error de DRF
            raise serializers.ValidationError(e.message_dict)
        
        return data
