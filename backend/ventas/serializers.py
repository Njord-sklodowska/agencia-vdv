
from rest_framework import serializers
from .models import OperacionVenta, FormaPago, Anticipo
import datetime
from django.core.exceptions import ValidationError
from inventario.models import Vehiculo



class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = ['id', 'operacion', 'tipo_pago', 'monto', 'cotizacion_dolar', 'fecha_registro']
        read_only_fields = ['fecha_registro']

    def validate(self, data):
        instance = self.instance or FormaPago()
        for attr, value in data.items():
            setattr(instance, attr, value)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data


class AnticipoSerializer(serializers.ModelSerializer):
    vehiculo_detalle = serializers.CharField(source='vehiculo.__str__', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.get_full_name', read_only=True)

    class Meta:
        model = Anticipo
        fields = [
            'id',
            'vehiculo', 'vehiculo_detalle',
            'cliente', 'cliente_nombre',
            'usuario_registro',
            'operacion_aplicado',
            'monto', 'forma_pago',
            'fecha_anticipo', 'estado', 'observaciones',
            'fecha_alta', 'updated_at',
        ]
        read_only_fields = ['fecha_alta', 'updated_at']

    def validate_fecha_anticipo(self, value):
        hoy = datetime.date.today()
        if value > hoy:
            raise serializers.ValidationError('La fecha del anticipo no puede ser futura.')
        if (hoy - value).days > 30:
            raise serializers.ValidationError('La fecha del anticipo no puede ser anterior a 30 días.')
        return value

    def validate(self, data):
        instance = self.instance or Anticipo()
        for attr, value in data.items():
            setattr(instance, attr, value)
        try:
            instance.clean()
        except Exception as e:
            raise serializers.ValidationError(e.message_dict)
        return data
    
class OperacionVentaSerializer(serializers.ModelSerializer):
    vehiculo_detalle = serializers.CharField(source='vehiculo_vendido.__str__', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.get_full_name', read_only=True)
    formas_pago = FormaPagoSerializer(many=True, read_only=True)
    precio_original = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    precio_final = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    
    class Meta:
        model = OperacionVenta
        fields = [
            'id',
            'sucursal',
            'cliente', 'cliente_nombre',
            'cliente_cotitular',
            'vehiculo_vendido', 'vehiculo_detalle',
            'vehiculo_usado_entregado',
            'vendedor', 'usuario_registro',
            'anticipo',
            'fecha_operacion',
            'precio_original', 'descuento_aplicado', 'valor_vehiculo_usado', 'precio_final',
            'estado', 'numero_boleto', 'ruta_boleto_pdf', 'observaciones',
            'fecha_cambio_estado', 'fecha_alta', 'updated_at',
            'formas_pago',
        ]
        read_only_fields = ['fecha_alta', 'updated_at', 'fecha_cambio_estado', 'precio_original', 'precio_final', 'valor_vehiculo_usado']
        extra_kwargs = {
            'sucursal': {'required': True},
            'vendedor': {'required': True},
            'usuario_registro': {'required': True},
            'vehiculo_vendido': {'required': True},
        }

    def create(self, validated_data):
        vehiculo = validated_data['vehiculo_vendido']
        validated_data['precio_original'] = vehiculo.precio
        
        vehiculo_usado = validated_data.get('vehiculo_usado_entregado')
        if vehiculo_usado:
            validated_data['valor_vehiculo_usado'] = vehiculo_usado.precio_costo
        
        return super().create(validated_data)
    
    def validate_estado(self, value):
        if value == 'confirmada':
            raise serializers.ValidationError(
                'Para confirmar una operación use la acción confirmar.'
            )
        return value

    def validate_fecha_operacion(self, value):
        hoy = datetime.date.today()
        if value > hoy:
            raise serializers.ValidationError('La fecha de operación no puede ser futura.')
        if (hoy - value).days > 30:
            raise serializers.ValidationError('La fecha de operación no puede ser anterior a 30 días.')
        return value

    def validate(self, data):
    # Primero bloquear modificación de operaciones cerradas
        if self.instance and self.instance.estado in ['confirmada', 'completada', 'cancelada']:
            raise serializers.ValidationError(
                'No se puede modificar una operación que ya fue confirmada, completada o cancelada.'
            )

        # Validar vehículo no vendido
        vehiculo = data.get('vehiculo_vendido')
        if vehiculo and vehiculo.estado == 'vendido':
            raise serializers.ValidationError(
                {'vehiculo_vendido': 'No se puede crear una operación para un vehículo ya vendido.'}
            )

        # Validar anticipo corresponde al vehículo
        anticipo = data.get('anticipo')
        if anticipo and vehiculo and anticipo.vehiculo != vehiculo:
            raise serializers.ValidationError(
                {'anticipo': 'El anticipo no corresponde al vehículo seleccionado.'}
            )

        instance = self.instance or OperacionVenta()
        for attr, value in data.items():
            setattr(instance, attr, value)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return data