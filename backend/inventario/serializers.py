
from rest_framework import serializers
from config.serializers import ValidatedModelSerializer
from .models import Marca, Modelo, Vehiculo, Fotografia_Vehiculo, Taller, VehiculoUsado, TrasladoVehiculo
import datetime 

class MarcaSerializer(ValidatedModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'updated_at']
        read_only_fields = ['updated_at']


class ModeloSerializer(ValidatedModelSerializer):
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)

    class Meta:
        model = Modelo
        fields = ['id', 'marca', 'marca_nombre', 'nombre', 'carroceria', 'updated_at']
        read_only_fields = ['updated_at']


class FotografiaVehiculoSerializer(ValidatedModelSerializer):
    class Meta:
        model = Fotografia_Vehiculo
        fields = ['id', 'archivo', 'nombre_original', 'es_portada', 'orden', 'tamano_bytes', 'mime_type', 'fecha_alta']
        read_only_fields = ['tamano_bytes', 'mime_type', 'fecha_alta']


class VehiculoSerializer(ValidatedModelSerializer):
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    modelo_nombre = serializers.CharField(source='modelo.nombre', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    fotos = FotografiaVehiculoSerializer(many=True, read_only=True)

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
            'fotos',
        ]
        read_only_fields = ['fecha_alta', 'fecha_cambio_estado', 'updated_at']

    def validate(self, data):
        precio = data.get('precio')
        precio_costo = data.get('precio_costo')
        
        if precio and precio_costo and precio < precio_costo:
            self._precio_bajo_costo = True
        
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if getattr(self, '_precio_bajo_costo', False):
            data['advertencia'] = 'El precio de venta es inferior al costo.'
        return data

class TallerSerializer(ValidatedModelSerializer):
    class Meta:
        model = Taller
        fields = ['id', 'nombre', 'direccion', 'telefono', 'email', 'estado', 'fecha_alta', 'updated_at']
        read_only_fields = ['fecha_alta', 'updated_at']


class VehiculoUsadoSerializer(ValidatedModelSerializer):
    vehiculo_detalle = serializers.CharField(source='vehiculo.__str__', read_only=True)
    taller_nombre = serializers.CharField(source='taller.nombre', read_only=True)
    usuario_autoriza_nombre = serializers.CharField(source='usuario_autoriza.get_full_name', read_only=True)

    class Meta:
        model = VehiculoUsado
        fields = [
            'id',
            'vehiculo', 'vehiculo_detalle',
            'taller', 'taller_nombre',
            'usuario_autoriza', 'usuario_autoriza_nombre',
            'precio_info_auto', 'porcentaje_deduccion', 'precio_tasacion_final',
            'estado_cubierta', 'estado_motor', 'estado_chapa_pintura', 'estado_interior',
            'fecha_evaluacion', 'fecha_ingreso', 'observaciones',
            'fecha_alta', 'updated_at',
        ]
        read_only_fields = ['fecha_alta', 'updated_at']

    def validate_precio_tasacion_final(self, value):
        taller = self.initial_data.get('taller')
        precio_info_auto = self.initial_data.get('precio_info_auto')
        porcentaje = self.initial_data.get('porcentaje_deduccion')

        if taller and precio_info_auto and porcentaje:
            esperado = float(precio_info_auto) - (float(precio_info_auto) * float(porcentaje) / 100)
            if abs(float(value) - esperado) > 0.01:
                raise serializers.ValidationError(
                    f'Con taller el precio debe ser {esperado:.2f} según Info Auto y porcentaje ingresado.'
                )
        return value
    def validate_porcentaje_deduccion(self, value):
        if value is not None and (value < 15 or value > 20):
            raise serializers.ValidationError(
                'El porcentaje de deducción debe estar entre 15 y 20.'
            )
        return value      

    def validate(self, data):
        taller = data.get('taller')

        if not taller:
            for campo in ['precio_info_auto', 'porcentaje_deduccion', 'fecha_evaluacion']:
                if data.get(campo) is not None:
                    raise serializers.ValidationError(
                        {campo: 'Este campo debe ser nulo cuando no hay taller asignado.'}
                    )
        else:
            for campo in ['precio_info_auto', 'porcentaje_deduccion', 'fecha_evaluacion',
                          'estado_cubierta', 'estado_motor', 'estado_chapa_pintura', 'estado_interior']:
                if not data.get(campo):
                    raise serializers.ValidationError(
                        {campo: 'Este campo es obligatorio cuando hay taller asignado.'}
                    )

        instance = self.instance or VehiculoUsado()
        for attr, value in data.items():
            setattr(instance, attr, value)
        try:
            instance.clean()
        except Exception as e:
            raise serializers.ValidationError(e.message_dict)
        
        fecha_ingreso = data.get('fecha_ingreso')
        fecha_evaluacion = data.get('fecha_evaluacion')
        if fecha_ingreso and fecha_evaluacion and fecha_evaluacion > fecha_ingreso:
            raise serializers.ValidationError(
                {'fecha_evaluacion': 'La fecha de evaluación no puede ser posterior a la fecha de ingreso.'}
            )

        return data

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
    
class TrasladoVehiculoSerializer(ValidatedModelSerializer):
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
        
    