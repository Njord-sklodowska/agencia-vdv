from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):

    rol_nombre = serializers.SerializerMethodField()
    sucursal_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'estado',
            'fecha_alta',
            'updated_at',
            'rol',
            'rol_nombre',
            'sucursal',
            'sucursal_nombre'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_rol_nombre(self, obj):
        if obj.rol:
            return obj.rol.nombre
        return None

    def get_sucursal_nombre(self, obj):
        if obj.sucursal:
            return obj.sucursal.nombre
        return None

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Ya existe un usuario con este email."
            )
        return value
    
    def validate_rol(self, value):
        if not value:
            raise serializers.ValidationError(
                "El rol es obligatorio."
            )
        return value

    def validate_sucursal(self, value):
        if not value:
            raise serializers.ValidationError(
                "La sucursal es obligatoria."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        user = Usuario(**validated_data)

        if password:
            user.set_password(password)

        user.save()
        return user