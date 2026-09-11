
from rest_framework import serializers
from .models import Marca, Modelo, Vehiculo, Fotografia_Vehiculo, Taller, VehiculoUsado, TrasladoVehiculo
import datetime 
from decimal import Decimal

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'updated_at']
        read_only_fields = ['updated_at']


class ModeloSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)

    class Meta:
        model = Modelo
        fields = ['id', 'marca', 'marca_nombre', 'nombre', 'carroceria', 'updated_at']
        read_only_fields = ['updated_at']


class FotografiaVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotografia_Vehiculo
        fields = ['id', 'archivo', 'nombre_original', 'es_portada', 'orden', 'tamano_bytes', 'mime_type', 'fecha_alta']
        read_only_fields = ['tamano_bytes', 'mime_type', 'fecha_alta']


class VehiculoSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    modelo_nombre = serializers.CharField(source='modelo.nombre', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    fotos = FotografiaVehiculoSerializer(many=True, read_only=True)
    confirmar_precio_bajo_costo = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Vehiculo
        fields = [
            'id',
            'sucursal', 'sucursal_nombre',
            'marca', 'marca_nombre',
            'modelo', 'modelo_nombre',
            'condicion_vehiculo', 'vin', 'patente',
            'anio', 'color', 'precio_costo', 'precio',
            'descripcion_tecnica', 'estado', 'kilometraje',
            'activo', 'entregado',
            'combustible', 'transmision', 'puertas', 'motor', 'traccion',
            'numero_serie_motor', 'procedencia',
            'fecha_alta', 'fecha_cambio_estado', 'updated_at',
            'fotos','confirmar_precio_bajo_costo',
        ]
        read_only_fields = ['fecha_alta', 'fecha_cambio_estado', 'updated_at']

    def validate(self, data):
        from django.core.exceptions import ValidationError
        errores = {}
        
        precio = data.get('precio', self.instance.precio if self.instance else None)
        precio_costo = data.get('precio_costo', self.instance.precio_costo if self.instance else None)
        confirmar = data.pop('confirmar_precio_bajo_costo', False)
# validacion precios
        if precio and precio_costo and precio < precio_costo and not confirmar:
            raise serializers.ValidationError({
                'advertencia': (
                    f'El precio de venta (${precio}) es inferior al costo registrado (${precio_costo}). '
                    f'Si desea guardarlo de todas formas, envíe confirmar_precio_bajo_costo: true.'
                )
            })
        
        if not data.get('numero_serie_motor', '').strip():
            errores['numero_serie_motor'] = 'El número de serie del motor es obligatorio.'

#validaciones de acuerdo a la condicion del vehiculo

        condicion = data.get('condicion_vehiculo')

        if condicion == 'usado':
            if not data.get('patente'):
                errores['patente'] = 'La patente es obligatoria para vehículos usados.'
            if (data.get('kilometraje') or 0) <= 0:
                errores['kilometraje'] = 'El kilometraje debe ser mayor a 0 para usados.'
            if not data.get('procedencia'):
                errores['procedencia'] = 'La procedencia es obligatoria para usados.'

        if condicion == '0km':
            if data.get('patente') and data.get('estado') != 'vendido':
                errores['patente'] = 'Un vehículo 0km no debe tener patente asignada.'
            if (data.get('kilometraje') or 0) > 500:
                errores['kilometraje'] = 'Un vehículo 0km no puede tener más de 500 km.'

        if errores:
            raise serializers.ValidationError(errores)

        if self.instance:
            # Update (PATCH/PUT): se reconstruye usando los campos reales del objeto,
            # pisados solo por lo que vino en este request. 
            campos = [
                'sucursal', 'marca', 'modelo', 'condicion_vehiculo', 'vin', 'patente',
                'anio', 'color', 'precio_costo', 'precio', 'descripcion_tecnica',
                'estado', 'kilometraje', 'activo', 'entregado', 'combustible',
                'transmision', 'puertas', 'motor', 'traccion', 'numero_serie_motor',
                'procedencia',
            ]
            datos_completos = {
                campo: data.get(campo, getattr(self.instance, campo))
                for campo in campos
            }
            instance = Vehiculo(**datos_completos)
            instance.pk = self.instance.pk
        else:
            # Create: no hay datos previos, se construye desde cero.
            instance = Vehiculo(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(
                getattr(e, 'message_dict', None) or {'non_field_errors': e.messages}
            )

        return data
    
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Agrega una advertencia visible en la respuesta si el precio de venta quedó por debajo del costo. No bloquea nada, solo informa - el bloqueo real esta en validate().

        if instance.precio and instance.precio_costo and instance.precio < instance.precio_costo:
            data['advertencias'] = ['El precio de venta es inferior al costo registrado.']

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            usuario = request.user
            es_vendedor = usuario.rol and usuario.rol.nombre == 'vendedor' and not usuario.is_superuser
            if es_vendedor:
                data.pop('precio_costo', None)

        return data

class VehiculoUsadoSerializer(serializers.ModelSerializer):
    vehiculo_detalle = serializers.CharField(source='vehiculo.__str__', read_only=True)
    taller_nombre = serializers.CharField(source='taller.nombre', read_only=True)
    usuario_autoriza_nombre = serializers.CharField(source='usuario_autoriza.get_full_name', read_only=True)
    precio_tasacion_final = serializers.DecimalField(max_digits=14, decimal_places=2, required=False)
    
    class Meta:
        model = VehiculoUsado
        fields = [
            'id',
            'vehiculo', 'vehiculo_detalle','taller', 'taller_nombre',
            'usuario_autoriza', 'usuario_autoriza_nombre',
            'precio_info_auto', 'porcentaje_deduccion', 'precio_tasacion_final',
            'estado_cubierta', 'estado_motor', 'estado_chapa_pintura', 'estado_interior',
            'fecha_evaluacion', 'fecha_ingreso', 'observaciones','fecha_alta', 'updated_at',
        ]
        read_only_fields = ['fecha_alta', 'updated_at']

    def validate_porcentaje_deduccion(self, value):
        if value is not None and (value < 1 or value > 20):
            raise serializers.ValidationError(
                'El porcentaje de deducción debe estar entre 1 y 20.'
            )
        return value

    def validate_fecha_ingreso(self, value):
        hoy = datetime.date.today()
        if value > hoy:
            raise serializers.ValidationError('La fecha de ingreso no puede ser futura.')
        if (hoy - value).days > 30:
            raise serializers.ValidationError('La fecha de ingreso no puede ser anterior a 30 días.')
        return value

    def validate_fecha_evaluacion(self, value):
        if value is None:
            return value
        hoy = datetime.date.today()
        if value > hoy:
            raise serializers.ValidationError('La fecha de evaluación no puede ser futura.')
        if (hoy - value).days > 30:
            raise serializers.ValidationError('La fecha de evaluación no puede ser anterior a 30 días.')
        return value

    def validate_precio_tasacion_final(self, value):
        if self.instance:
            taller = self.initial_data.get('taller', self.instance.taller_id)
            precio_info_auto = self.initial_data.get('precio_info_auto', self.instance.precio_info_auto)
            porcentaje = self.initial_data.get('porcentaje_deduccion', self.instance.porcentaje_deduccion)
        else:
            taller = self.initial_data.get('taller')
            precio_info_auto = self.initial_data.get('precio_info_auto')
            porcentaje = self.initial_data.get('porcentaje_deduccion')

        if taller and precio_info_auto and porcentaje:
            try:
                esperado = Decimal(str(precio_info_auto)) - (Decimal(str(precio_info_auto)) * Decimal(str(porcentaje)) / Decimal('100'))
                if abs(Decimal(str(value)) - esperado) > Decimal('0.01'):
                    raise serializers.ValidationError(
                        f'Con taller el precio debe ser {esperado:.2f} según Info Auto y porcentaje ingresado.'
                    )
            except serializers.ValidationError:
                raise
            except Exception:
                raise serializers.ValidationError('Los valores numéricos ingresados no son válidos.')
        return value

    def validate(self, data):
        # Combinar datos existentes con los nuevos para soportar PATCH parcial
        if self.instance:
            datos_completos = {
                'vehiculo': data.get('vehiculo', self.instance.vehiculo),
                'taller': data.get('taller', self.instance.taller),
                'precio_info_auto': data.get('precio_info_auto', self.instance.precio_info_auto),
                'porcentaje_deduccion': data.get('porcentaje_deduccion', self.instance.porcentaje_deduccion),
                'fecha_evaluacion': data.get('fecha_evaluacion', self.instance.fecha_evaluacion),
                'estado_cubierta': data.get('estado_cubierta', self.instance.estado_cubierta),
                'estado_motor': data.get('estado_motor', self.instance.estado_motor),
                'estado_chapa_pintura': data.get('estado_chapa_pintura', self.instance.estado_chapa_pintura),
                'estado_interior': data.get('estado_interior', self.instance.estado_interior),
                'fecha_ingreso': data.get('fecha_ingreso', self.instance.fecha_ingreso),
                'precio_tasacion_final': data.get('precio_tasacion_final', self.instance.precio_tasacion_final),
            }
        else:
            datos_completos = data

        vehiculo = datos_completos.get('vehiculo')
        if vehiculo and vehiculo.condicion_vehiculo != 'usado':
            raise serializers.ValidationError(
                {'vehiculo': 'Solo se pueden registrar vehículos con condición usado.'}
            )

        taller = datos_completos.get('taller')
        precio_info_auto = datos_completos.get('precio_info_auto')
        porcentaje = datos_completos.get('porcentaje_deduccion')

        # Info Auto, independiente del taller -
        # Si vienen ambos (precio_info_auto y porcentaje), el sistema calcula precio_tasacion_final automáticamente y lo sobreescribe.
        if precio_info_auto and porcentaje:
            calculado = Decimal(str(precio_info_auto)) - (Decimal(str(precio_info_auto)) * Decimal(str(porcentaje)) / Decimal('100'))
            data['precio_tasacion_final'] = calculado.quantize(Decimal('0.01'))
        else:
            # Sin Info Auto completo: el precio de tasación debe cargarse a mano.
            if not datos_completos.get('precio_tasacion_final'):
                raise serializers.ValidationError(
                    {'precio_tasacion_final': 'Debe indicar el precio de tasación cuando no se usa Info Auto (precio_info_auto + porcentaje_deduccion).'}
                )

        # Taller, independiente de Info Auto -
        # Si hay taller, los campos de inspección técnica son obligatorios.
        if taller:
            for campo in ['estado_cubierta', 'estado_motor', 'estado_chapa_pintura', 'estado_interior', 'fecha_evaluacion']:
                if not datos_completos.get(campo):
                    raise serializers.ValidationError(
                        {campo: 'Este campo es obligatorio cuando hay taller asignado.'}
                    )
        else:
            for campo in ['estado_cubierta', 'estado_motor', 'estado_chapa_pintura', 'estado_interior', 'fecha_evaluacion']:
                if datos_completos.get(campo):
                    raise serializers.ValidationError(
                        {campo: 'Este campo solo aplica cuando hay taller asignado.'}
                    )

        fecha_ingreso = datos_completos.get('fecha_ingreso')
        fecha_evaluacion = datos_completos.get('fecha_evaluacion')
        if fecha_ingreso and fecha_evaluacion and fecha_evaluacion > fecha_ingreso:
            raise serializers.ValidationError(
                {'fecha_evaluacion': 'La fecha de evaluación no puede ser posterior a la fecha de ingreso.'}
            )

        return data

    def to_representation(self, instance):  # Agrega una advertencia visible en la respuesta si el precio de venta quedó por debajo del costo. No bloquea nada, solo informa - el bloqueo real está en validate().
        data = super().to_representation(instance)
        if instance.vehiculo and instance.precio_tasacion_final and instance.vehiculo.precio:
            if instance.precio_tasacion_final > instance.vehiculo.precio:
                data['advertencias'] = [
                    f'La tasación (${instance.precio_tasacion_final}) es superior al precio de venta actual del vehículo (${instance.vehiculo.precio}).'
                ]
        return data
    
class TallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = ['id', 'nombre', 'direccion', 'telefono', 'email', 'estado', 'fecha_alta', 'updated_at']
        read_only_fields = ['fecha_alta', 'updated_at']

class TrasladoVehiculoSerializer(serializers.ModelSerializer):
    vehiculo_detalle = serializers.CharField(source='vehiculo.__str__', read_only=True)
    sucursal_origen_nombre = serializers.CharField(source='sucursal_origen.nombre', read_only=True)
    sucursal_destino_nombre = serializers.CharField(source='sucursal_destino.nombre', read_only=True)
    usuario_autoriza_nombre = serializers.CharField(source='usuario_autoriza.get_full_name', read_only=True)
    usuario_registro_nombre = serializers.CharField(source='usuario_registro.get_full_name', read_only=True)

    class Meta:
        model = TrasladoVehiculo
        fields = [
            'id',
            'vehiculo', 'vehiculo_detalle',
            'sucursal_origen', 'sucursal_origen_nombre',
            'sucursal_destino', 'sucursal_destino_nombre',
            'usuario_autoriza', 'usuario_autoriza_nombre',
            'usuario_registro', 'usuario_registro_nombre',
            'costo_traslado', 'fecha_traslado', 'motivo', 'estado',
            'fecha_alta', 'updated_at',
        ]
        read_only_fields = ['fecha_alta', 'updated_at']

    def validate(self, data):
        if data.get('sucursal_origen') == data.get('sucursal_destino'):
            raise serializers.ValidationError(
                {'sucursal_destino': 'La sucursal destino no puede ser igual a la de origen.'}
            )
        return data

    def validate_fecha_traslado(self, value):
        hoy = datetime.date.today()
        if value > hoy:
            raise serializers.ValidationError('La fecha de traslado no puede ser futura.')
        if (hoy - value).days > 30:
            raise serializers.ValidationError('La fecha de traslado no puede ser anterior a 30 días.')
        return value