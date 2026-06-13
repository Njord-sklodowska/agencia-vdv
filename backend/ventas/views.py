
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import OperacionVenta, FormaPago, Anticipo
from .serializers import OperacionVentaSerializer, FormaPagoSerializer, AnticipoSerializer
from rest_framework import serializers
from inventario.models import Vehiculo


class OperacionVentaViewSet(viewsets.ModelViewSet):
    serializer_class = OperacionVentaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # TODO: filtrar por sucursal del usuario cuando Sergio termine roles
        return OperacionVenta.objects.all()

    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        operacion = self.get_object()

        if operacion.estado != 'borrador':
            return Response(
                {'detail': 'Solo se pueden confirmar operaciones en estado borrador.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar suma de formas de pago
        total_pagado = sum(fp.monto for fp in operacion.formas_pago.all())

        if operacion.anticipo and operacion.anticipo.estado == 'pendiente':
            total_pagado += operacion.anticipo.monto

        if operacion.valor_vehiculo_usado:
            total_pagado += operacion.valor_vehiculo_usado

        if not operacion.formas_pago.exists() and not operacion.vehiculo_usado_entregado:
            return Response(
                {'detail': 'Debe agregar al menos una forma de pago antes de confirmar.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if total_pagado != operacion.precio_final:
            return Response(
                {'detail': f'La suma de formas de pago ({total_pagado}) no coincide con el precio final ({operacion.precio_final}).'},
                status=status.HTTP_400_BAD_REQUEST
            )
        

        with transaction.atomic():
            vehiculo = Vehiculo.objects.select_for_update().get(pk=operacion.vehiculo_vendido.pk)
            if vehiculo.estado == 'vendido':
                return Response(
                    {'detail': 'El vehículo ya fue vendido en otra operación.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            operacion.estado = 'confirmada'
            operacion.save(skip_validation=True)
            vehiculo.estado = 'vendido'
            vehiculo.save(skip_validation=True)
            if operacion.anticipo and operacion.anticipo.estado == 'pendiente':
                operacion.anticipo.estado = 'aplicado'
                operacion.anticipo.operacion_aplicado = operacion
                operacion.anticipo.save(skip_validation=True)

        return Response({'detail': 'Operación confirmada correctamente.'})

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        operacion = self.get_object()

        if operacion.estado not in ['borrador', 'confirmada']:
            return Response(
                {'detail': 'Solo se pueden cancelar operaciones en estado borrador o confirmada.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        motivo = request.data.get('observaciones')
        if not motivo:
            return Response(
                {'detail': 'Debe indicar el motivo de la cancelación.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            estado_anterior = operacion.vehiculo_vendido.estado
            
            operacion.estado = 'cancelada'
            operacion.observaciones = motivo
            operacion.save(skip_validation=True)

            # Revertir estado del vehículo
            vehiculo = operacion.vehiculo_vendido
            vehiculo.estado = 'reservado' if operacion.anticipo else 'en_stock'
            vehiculo.save(skip_validation=True)

            # Revertir anticipo a pendiente si estaba aplicado
            if operacion.anticipo and operacion.anticipo.estado == 'aplicado':
                operacion.anticipo.estado = 'pendiente'
                operacion.anticipo.operacion_aplicado = None
                operacion.anticipo.save(skip_validation=True)

        return Response({'detail': 'Operación cancelada correctamente.'})

    @action(detail=True, methods=['post'])
    def completar(self, request, pk=None):
        operacion = self.get_object()

        if operacion.estado != 'confirmada':
            return Response(
                {'detail': 'Solo se pueden completar operaciones confirmadas.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        operacion.estado = 'completada'
        operacion.save(skip_validation=True)
        return Response({'detail': 'Operación completada correctamente.'})


class FormaPagoViewSet(viewsets.ModelViewSet):
    serializer_class = FormaPagoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FormaPago.objects.filter(operacion_id=self.kwargs['operacion_pk'])

    def perform_create(self, serializer):
        from rest_framework.exceptions import ValidationError
        operacion = OperacionVenta.objects.get(pk=self.kwargs['operacion_pk'])
        
        if operacion.estado != 'borrador':
            raise ValidationError('No se pueden agregar formas de pago a una operación que no está en borrador.')
        
        total_actual = sum(fp.monto for fp in operacion.formas_pago.all())
        monto_nuevo = serializer.validated_data.get('monto', 0)
        
        if total_actual + monto_nuevo > operacion.precio_final:
            raise ValidationError(
                f'El monto supera el precio final. Disponible: {operacion.precio_final - total_actual}'
            )
        
        serializer.save(operacion=operacion)


class AnticipoViewSet(viewsets.ModelViewSet):
    serializer_class = AnticipoSerializer
    permission_classes = [IsAuthenticated]
    # TODO: solo administrativo y superiores pueden registrar anticipos

    def get_queryset(self):
        # TODO: filtrar por sucursal del usuario cuando Sergio termine roles
        return Anticipo.objects.all()