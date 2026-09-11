
from rest_framework import serializers
from .models import OperacionVenta, FormaPago, Anticipo, TituloCredito, RegistroCobro, CreditoInterno, CuotaCredito, EntidadFinanciera, FinanciamientoExterno
import datetime
from django.core.exceptions import ValidationError
from inventario.models import Vehiculo
from decimal import Decimal


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
            raise serializers.ValidationError(
                getattr(e, 'message_dict', None) or {'non_field_errors': e.messages}
            )
        return data


class AnticipoSerializer(serializers.ModelSerializer):
    vehiculo_detalle = serializers.CharField(source='vehiculo.__str__', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.get_full_name', read_only=True)
    confirmar_duplicado = serializers.BooleanField(write_only=True, required=False, default=False)

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
            'confirmar_duplicado', 
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
        vehiculo = data.get('vehiculo')
        confirmar = data.pop('confirmar_duplicado', False)  # lo sacamos antes de limpiar

        # Advertencia de duplicado
        if vehiculo and not confirmar:
            anticipos_activos = Anticipo.objects.filter(
                vehiculo=vehiculo,
                estado='pendiente'
            )
            if anticipos_activos.exists():
                existente = anticipos_activos.first()
                raise serializers.ValidationError({
                    'advertencia': (
                        f'Ya existe un anticipo pendiente para este vehículo '
                        f'por ${existente.monto} del {existente.fecha_anticipo}. '
                        f'Si desea registrar otro de todas formas, '
                        f'envíe confirmar_duplicado: true.'
                    )
                })

        # Validación del modelo (sin cambios)
        instance = self.instance or Anticipo()
        for attr, value in data.items():
            setattr(instance, attr, value)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(
                getattr(e, 'message_dict', None) or {'non_field_errors': e.messages}
            )

        return data

    def create(self, validated_data):
        validated_data.pop('confirmar_duplicado', None) 
        return super().create(validated_data)
    
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

        # Validar si el anticipo corresponde al vehículo
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
            raise serializers.ValidationError(
                getattr(e, 'message_dict', None) or {'non_field_errors': e.messages}
            )

        return data
    
class TituloCreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TituloCredito
        fields = [
            'id',
            'forma_pago', 'anticipo',
            'tipo', 'numero_documento', 'banco_emisor', 'titular',
            'plazo_dias',
            'fecha_recepcion', 'fecha_cobro', 'fecha_vencimiento_manual',
            'fecha_acreditacion', 'forma_acreditacion',
            'monto', 'interes_mora',
            'estado', 'observaciones',
            'fecha_alta', 'updated_at',
        ]
        read_only_fields = ['fecha_alta', 'updated_at', 'fecha_cobro']

    def validate_banco_emisor(self, value):
        tipo = self.initial_data.get('tipo')
        if tipo == 'cheque' and not value:
            raise serializers.ValidationError('El banco emisor es obligatorio para cheques.')
        return value

    def validate_plazo_dias(self, value):
        if value is None:
            return value
        if value not in [0, 30, 60, 90]:
            raise serializers.ValidationError('El plazo debe ser 0, 30, 60 o 90 días.')
        return value

    def validate(self, data):
        tipo = data.get('tipo')
        banco_emisor = data.get('banco_emisor')
        interes_mora = data.get('interes_mora', 0)
        forma_pago = data.get('forma_pago')
        anticipo = data.get('anticipo')
        estado = data.get('estado')
        observaciones = data.get('observaciones', '')

        # banco_emisor obligatorio para cheques
        if tipo == 'cheque' and not banco_emisor:
            raise serializers.ValidationError(
                {'banco_emisor': 'El banco emisor es obligatorio para cheques.'}
            )

        # interes_mora solo para pagarés
        if tipo == 'cheque' and interes_mora and interes_mora > 0:
            raise serializers.ValidationError(
                {'interes_mora': 'El interés de mora solo aplica para pagarés.'}
            )

    # forma_pago y anticipo no pueden ser ambos null ni ambos completos
        if not forma_pago and not anticipo:
            raise serializers.ValidationError(
                'Debe referenciar una forma de pago o un anticipo.'
            )
        if forma_pago and anticipo:
            raise serializers.ValidationError(
                'No puede referenciar una forma de pago y un anticipo al mismo tiempo.'
            )

    # observaciones obligatorias cuando es rechazado o en gestion
        if estado in ['rechazado', 'en_gestion'] and not observaciones:
            raise serializers.ValidationError(
                {'observaciones': 'Debe indicar el motivo cuando el estado es rechazado o en gestión.'}
            )

        # fecha de cobro máximo 90 días desde recepcion
        fecha_recepcion = data.get('fecha_recepcion')
        plazo_dias = data.get('plazo_dias', 0)
        if fecha_recepcion and plazo_dias:
            fecha_cobro = fecha_recepcion + datetime.timedelta(days=plazo_dias)
            delta = (fecha_cobro - fecha_recepcion).days
            if delta > 90:
                raise serializers.ValidationError(
                    {'plazo_dias': 'La fecha de cobro no puede superar los 90 días desde la recepción.'}
                )
# Ejecuta las validaciones del modelo (clean()) para atrapar errores y devolverlos como error 400.
        instance = self.instance or TituloCredito()
        for attr, value in data.items():
            setattr(instance, attr, value)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(
                getattr(e, 'message_dict', None) or {'non_field_errors': e.messages}
            )

        return data


class RegistroCobroSerializer(serializers.ModelSerializer):
    titulo_detalle = serializers.CharField(source='titulo.__str__', read_only=True)
    usuario_registro_nombre = serializers.CharField(
        source='usuario_registro.get_full_name', read_only=True
    )

    class Meta:
        model = RegistroCobro
        fields = [
            'id', 'titulo', 'titulo_detalle', 'usuario_registro',
            'fecha_pago_real', 'monto_pagado', 'pago_con_mora',
            'monto_mora_pagado', 'forma_cobro', 'forma_acreditacion_cheque',
            'observaciones', 'fecha_alta',
        ]
        read_only_fields = ['fecha_alta']

    def validate(self, data):
        titulo = data.get('titulo')
        pago_con_mora = data.get('pago_con_mora', False)
        monto_mora_pagado = data.get('monto_mora_pagado', 0)

        if titulo:
            #Evita registrar cobros duplicados
            if titulo.estado == 'cobrado':
                raise serializers.ValidationError(
                    {'titulo': 'Este título de crédito ya se encuentra registrado como cobrado.'}
                )
            # mora solo para pagarés
            if pago_con_mora and titulo.tipo != 'pagare':
                raise serializers.ValidationError(
                    {'pago_con_mora': 'El pago con mora solo aplica para pagarés.'}
                )
            if monto_mora_pagado > 0 and titulo.tipo != 'pagare':
                raise serializers.ValidationError(
                    {'monto_mora_pagado': 'El monto de mora solo aplica para pagarés.'}
                )
            
        return data
    

class EntidadFinancieraSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntidadFinanciera
        fields = ['id', 'nombre', 'estado', 'fecha_alta', 'updated_at']
        read_only_fields = ['fecha_alta', 'updated_at']


class FinanciamientoExternoSerializer(serializers.ModelSerializer):
    entidad_nombre = serializers.CharField(source='entidad.nombre', read_only=True)

    class Meta:
        model = FinanciamientoExterno
        fields = [
            'id',
            'operacion',
            'forma_pago',
            'entidad', 'entidad_nombre',
            'monto_aprobado', 'numero_credito', 'fecha_aprobacion',
            'fecha_alta', 'updated_at',
        ]
        read_only_fields = ['fecha_alta', 'updated_at']

    def validate(self, data):
        instance = self.instance or FinanciamientoExterno()
        for attr, value in data.items():
            setattr(instance, attr, value)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(
                getattr(e, 'message_dict', None) or {'non_field_errors': e.messages}
            )
        return data


class CuotaCreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuotaCredito
        fields = [
            'id', 'credito_interno', 'numero_cuota', 'monto_cuota', 'fecha_vencimiento',
            'monto_pagado', 'fecha_pago_real', 'forma_pago_cuota', 'monto_mora',
            'estado', 'observaciones', 'fecha_alta', 'updated_at',
        ]
        read_only_fields = [
            'credito_interno', 'numero_cuota', 'monto_cuota', 'fecha_vencimiento',
            'fecha_alta', 'updated_at',
        ]

    def validate(self, data):
        instance = self.instance or CuotaCredito()
        for attr, value in data.items():
            setattr(instance, attr, value)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data


class CreditoInternoSerializer(serializers.ModelSerializer):
    cuotas = CuotaCreditoSerializer(many=True, read_only=True)
    fecha_primera_cuota = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = CreditoInterno
        fields = [
            'id', 'operacion', 'forma_pago',
            'monto_financiado', 'cantidad_cuotas', 'tasa_interes_mensual', 'fecha_primera_cuota',  
            'monto_cuota', 'monto_total',
            'estado', 'observaciones', 
            'fecha_alta', 'updated_at', 'cuotas',
        ]
        read_only_fields = [
        'monto_cuota', 
        'monto_total', 
        'estado', 
        'fecha_alta', 
        'updated_at'
    ]

    def validate(self, data):
        instance = self.instance or CreditoInterno()
        for attr, value in data.items():
            setattr(instance, attr, value)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(
                getattr(e, 'message_dict', None) or {'non_field_errors': e.messages}
            )
        return data