from datetime import timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from inventario.models import Vehiculo

from .models import DocumentacionVehiculo, Gestor, TipoDocumento
from .serializers import (
    DocumentacionVehiculoSerializer,
    GestorSerializer,
    TipoDocumentoSerializer,
)


class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.filter(activo=True)
    serializer_class = TipoDocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]


class GestorViewSet(viewsets.ModelViewSet):
    queryset = Gestor.objects.filter(estado="activo")
    serializer_class = GestorSerializer
    permission_classes = [permissions.IsAuthenticated]


class DocumentacionVehiculoViewSet(viewsets.ModelViewSet):
    queryset = DocumentacionVehiculo.objects.filter(activo=True)
    serializer_class = DocumentacionVehiculoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["vehiculo", "estado_documento", "gestor", "tipo_documento"]

    @action(detail=False, methods=["get"], url_path="buscar")
    def buscar_por_patente_o_vin(self, request):
        """Búsqueda de documentación por patente o VIN del vehículo."""
        query = request.query_params.get("q")
        if not query:
            return Response(
                {"error": "Debe proporcionar una patente o VIN en el parámetro 'q'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        docs = DocumentacionVehiculo.objects.filter(activo=True).filter(
            Q(vehiculo__patente__iexact=query) | Q(vehiculo__vin__iexact=query)
        )

        serializer = self.get_serializer(docs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="estado-vehiculo/(?P<vehiculo_id>[^/.]+)")
    def estado_vehiculo(self, request, vehiculo_id=None):
        """
        Informa si la documentación de un vehículo está Completa,
        y en caso contrario, qué tipos de documento obligatorios faltan.
        Pensado para ser consultado por la app 'ventas' antes de permitir
        la entrega del vehículo al cliente.
        """
        vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)

        faltantes = DocumentacionVehiculo.documentos_faltantes(vehiculo)

        return Response(
            {
                "vehiculo_id": vehiculo.id,
                "documentacion_completa": len(faltantes) == 0,
                "documentos_faltantes": faltantes,
            }
        )

    @action(detail=False, methods=["get"], url_path="alertas-vencimiento")
    def alertas_vencimiento(self, request):
        """
        Documentos con fecha_vencimiento vencida o próxima a vencer
        (por defecto, dentro de los próximos 30 días). Uso: dashboard de
        alertas para VTV / Informe de Multas.
        """
        dias = int(request.query_params.get("dias", 30))
        limite = timezone.now().date() + timedelta(days=dias)

        docs = DocumentacionVehiculo.objects.filter(
            activo=True,
            fecha_vencimiento__isnull=False,
            fecha_vencimiento__lte=limite,
        ).order_by("fecha_vencimiento")

        serializer = self.get_serializer(docs, many=True)
        return Response(serializer.data)