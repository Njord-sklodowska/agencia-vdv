
# inventario/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Value, F
from django.db.models.functions import Concat
from .models import Marca, Modelo, Vehiculo, Fotografia_Vehiculo, Taller, VehiculoUsado, TrasladoVehiculo
from .serializers import (
    MarcaSerializer, ModeloSerializer, VehiculoSerializer,
    FotografiaVehiculoSerializer, TallerSerializer,
    VehiculoUsadoSerializer, TrasladoVehiculoSerializer
)
from config.pagination import StandardResultsSetPagination
from config.mixins import AuditMixin


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]
    # TODO: solo superadministrador y administrativo pueden crear/editar/eliminar


class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['marca']
    # TODO: solo superadministrador y administrativo pueden crear/editar/eliminar


class VehiculoViewSet(AuditMixin, viewsets.ModelViewSet):
    modulo_name = "Inventario"
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['marca', 'modelo', 'estado']
    
    # Campos para búsqueda y ordenamiento
    search_fields = ['full_description', 'vin', 'patente', 'color', 'descripcion_tecnica']
    ordering_fields = ['full_description', 'precio', 'anio', 'kilometraje', 'fecha_alta', 'vin', 'patente', 'marca_nombre', 'modelo_nombre']

    def get_queryset(self):
        # Anotamos el campo full_description combinando Marca y Modelo para búsqueda y ordenamiento unificado
        # También anotamos marca_nombre y modelo_nombre para permitir el ordenamiento alfabético directo
        return Vehiculo.objects.annotate(
            full_description=Concat('marca__nombre', Value(' '), 'modelo__nombre'),
            marca_nombre=F('marca__nombre'),
            modelo_nombre=F('modelo__nombre')
        ).all()

    def perform_create(self, serializer):
        # TODO: asignar sucursal del usuario automáticamente
        # serializer.save(sucursal=self.request.user.sucursal)
        serializer.save()

    # Acción para obtener estadísticas del dashboard
    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        queryset = self.get_queryset()
        total_vehiculos = queryset.count()
        nuevos = queryset.filter(condicion_vehiculo='0km').count()
        usados = queryset.filter(condicion_vehiculo='usado').count()
        pendientes_entrega = queryset.filter(estado='vendido', entregado=False).count()
        
        # Suma total de precios de venta
        valor_total = sum(float(v.precio) for v in queryset if v.precio)
        
        return Response({
            'total_vehiculos': total_vehiculos,
            'nuevos': nuevos,
            'usados': usados,
            'pendientes_entrega': pendientes_entrega,
            'valor_total': valor_total,
        })

    # Acción para soft delete

    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        vehiculo = self.get_object()
        try:
            vehiculo.soft_delete()
            return Response({'detail': 'Vehículo desactivado correctamente.'})
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Acción para confirmar entrega
    @action(detail=True, methods=['post'])
    def entregar(self, request, pk=None):
        vehiculo = self.get_object()
        if vehiculo.estado != 'vendido':
            return Response(
                {'detail': 'Solo se puede entregar un vehículo vendido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if vehiculo.condicion_vehiculo == '0km' and not vehiculo.patente:
            return Response(
                {'detail': 'El vehículo 0km debe tener patente antes de ser entregado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        vehiculo.entregado = True
        vehiculo.save(skip_validation=True)
        return Response({'detail': 'Vehículo marcado como entregado.'})


class FotografiaVehiculoViewSet(viewsets.ModelViewSet):
    serializer_class = FotografiaVehiculoSerializer
    permission_classes = [IsAuthenticated]
    # TODO: solo administrativo y superiores pueden cargar fotos

    def get_queryset(self):
        return Fotografia_Vehiculo.objects.filter(vehiculo_id=self.kwargs['vehiculo_pk'])

    def perform_create(self, serializer):
        vehiculo = Vehiculo.objects.get(pk=self.kwargs['vehiculo_pk'])
        serializer.save(vehiculo=vehiculo)

    @action(detail=True, methods=['post'])
    def set_portada(self, request, pk=None):
        foto = self.get_object()
        vehiculo = foto.vehiculo
        
        # Desmarcar todas las fotos del vehículo como portada
        Fotografia_Vehiculo.objects.filter(vehiculo=vehiculo).update(es_portada=False)
        
        # Marcar la actual como portada
        foto.es_portada = True
        foto.save()
        
        return Response({'status': 'Foto establecida como portada'}, status=status.HTTP_200_OK)


class TallerViewSet(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    serializer_class = TallerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['estado']
    search_fields = ['nombre', 'direccion', 'telefono', 'email']
    ordering_fields = ['nombre', 'fecha_alta', 'estado']


class VehiculoUsadoViewSet(viewsets.ModelViewSet):
    queryset = VehiculoUsado.objects.all()
    serializer_class = VehiculoUsadoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['taller', 'usuario_autoriza']
    search_fields = ['vehiculo__patente', 'vehiculo__vin', 'observaciones', 'vehiculo__marca__nombre', 'vehiculo__modelo__nombre']
    ordering_fields = ['fecha_evaluacion', 'precio_tasacion_final', 'fecha_ingreso', 'marca_nombre', 'modelo_nombre']

    def get_queryset(self):
        return VehiculoUsado.objects.annotate(
            marca_nombre=F('vehiculo__marca__nombre'),
            modelo_nombre=F('vehiculo__modelo__nombre')
        ).all()


class TrasladoVehiculoViewSet(viewsets.ModelViewSet):
    serializer_class = TrasladoVehiculoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['estado', 'sucursal_origen', 'sucursal_destino']
    search_fields = ['vehiculo__patente', 'vehiculo__vin', 'motivo']
    ordering_fields = ['fecha_traslado', 'estado', 'costo_traslado']

    def get_queryset(self):
        return TrasladoVehiculo.objects.annotate(
            vehiculo_detalle=F('vehiculo__patente'),
            origen_nombre=F('sucursal_origen__nombre'),
            destino_nombre=F('sucursal_destino__nombre')
        ).all()

    # Acción para confirmar traslado
    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        traslado = self.get_object()
        if traslado.estado != 'pendiente':
            return Response(
                {'detail': 'Solo se pueden confirmar traslados en estado pendiente.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        traslado.estado = 'completado'
        traslado.save()
        # Actualiza la sucursal del vehículo
        traslado.vehiculo.sucursal = traslado.sucursal_destino
        traslado.vehiculo.save(skip_validation=True)
        return Response({'detail': 'Traslado confirmado. Sucursal del vehículo actualizada.'})

    # Acción para cancelar traslado
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        traslado = self.get_object()
        if traslado.estado != 'pendiente':
            return Response(
                {'detail': 'Solo se pueden cancelar traslados en estado pendiente.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        traslado.estado = 'cancelado'
        traslado.save()
        return Response({'detail': 'Traslado cancelado.'})