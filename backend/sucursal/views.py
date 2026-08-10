from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Sucursal
from .serializers import SucursalSerializer
from config.pagination import StandardResultsSetPagination
from config.mixins import AuditMixin


class SucursalViewSet(AuditMixin, viewsets.ModelViewSet):
    modulo_name = "Sucursales"
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['estado', 'provincia', 'ciudad']
    search_fields = ['nombre', 'direccion', 'ciudad', 'provincia']
    ordering_fields = ['nombre', 'ciudad', 'provincia', 'estado']

    def perform_destroy(self, instance):
        """Borrado lógico: cambia estado a 'inactiva' en lugar de eliminar"""
        instance.estado = 'inactiva'
        instance.save()
        # Registrar en auditoría
        desc = f"Se desactivó la sucursal {instance.nombre} (ID: {instance.pk})"
        self._log_action(instance, 'ELIMINAR', desc)

    def destroy(self, request, *args, **kwargs):
        """Override para devolver respuesta personalizada"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Sucursal desactivada correctamente.'}, status=status.HTTP_200_OK)
