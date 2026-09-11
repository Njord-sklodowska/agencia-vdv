from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Marca, Modelo, Vehiculo, Fotografia_Vehiculo, Taller, VehiculoUsado, TrasladoVehiculo
from .serializers import (
    MarcaSerializer, ModeloSerializer, VehiculoSerializer, FotografiaVehiculoSerializer,
    TallerSerializer, VehiculoUsadoSerializer, TrasladoVehiculoSerializer
)
from django.utils import timezone
from django.db.models import Q
from django.db import transaction


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]
    # TODO: solo superadministrador y administrativo pueden crear/editar/eliminar


class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer
    permission_classes = [IsAuthenticated]
    # solo superadministrador y administrativo pueden crear/editar/eliminar


class VehiculoViewSet(viewsets.ModelViewSet):
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Vehiculo.objects.all()
        return Vehiculo.objects.filter(sucursal=user.sucursal)

    def perform_create(self, serializer):
        serializer.save(sucursal=self.request.user.sucursal)

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
        vehiculo.fecha_entrega = timezone.now()
        vehiculo.save(skip_validation=True)
        return Response({'detail': 'Vehículo marcado como entregado.'})


class FotografiaVehiculoViewSet(viewsets.ModelViewSet):
    serializer_class = FotografiaVehiculoSerializer
    permission_classes = [IsAuthenticated]
    # solo administrativo y superiores pueden cargar fotos

    def get_queryset(self):
        return Fotografia_Vehiculo.objects.filter(vehiculo_id=self.kwargs['vehiculo_pk'])

    def create(self, request, *args, **kwargs):
        try:
            self.vehiculo = Vehiculo.objects.get(pk=self.kwargs['vehiculo_pk'])
        except Vehiculo.DoesNotExist:
            return Response(
                {'detail': 'Vehiculo no encontrado o inactivo.'},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(vehiculo=self.vehiculo)


class TallerViewSet(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    serializer_class = TallerSerializer
    permission_classes = [IsAuthenticated]
    # TODO: solo administrativo y superiores pueden crear/editar


class VehiculoUsadoViewSet(viewsets.ModelViewSet):
    queryset = VehiculoUsado.objects.all()
    serializer_class = VehiculoUsadoSerializer
    permission_classes = [IsAuthenticated]
    # autorización solo por superadministrador

    def get_queryset(self):
        vehiculo_id = self.request.query_params.get('vehiculo')
        if vehiculo_id:
            return VehiculoUsado.objects.filter(vehiculo_id=vehiculo_id)
        return VehiculoUsado.objects.all()


class TrasladoVehiculoViewSet(viewsets.ModelViewSet):
    serializer_class = TrasladoVehiculoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return TrasladoVehiculo.objects.all()
        return TrasladoVehiculo.objects.filter(
            Q(sucursal_origen=user.sucursal) | Q(sucursal_destino=user.sucursal)
        )

    # Acción para confirmar traslado
    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        traslado = self.get_object()
        if traslado.estado != 'pendiente':
            return Response(
                {'detail': 'Solo se pueden confirmar traslados en estado pendiente.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            vehiculo = Vehiculo.objects.select_for_update().get(pk=traslado.vehiculo_id)

            if vehiculo.estado != 'en_stock':
                return Response(
                    {'detail': f'No se puede confirmar el traslado: el vehículo está en estado "{vehiculo.estado}".'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            traslado.estado = 'completado'
            traslado.save()

            vehiculo.sucursal = traslado.sucursal_destino
            vehiculo.save(skip_validation=True)

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
