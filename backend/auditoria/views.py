from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F

from .models import LogAuditoria
from .serializers import LogAuditoriaSerializer
from config.pagination import StandardResultsSetPagination


class LogAuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogAuditoria.objects.all()
    serializer_class = LogAuditoriaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    # Filtros exactos por campo (mismo patrón que Clientes, Vehículos, etc.)
    filterset_fields = {
        'accion': ['exact'],
        'usuario': ['exact'],
        'fecha': ['gte', 'lte'],
    }

    search_fields = ['usuario__username', 'usuario__email', 'accion', 'modulo', 'tabla_afectada', 'descripcion']
    ordering_fields = ['fecha', 'usuario', 'accion', 'usuario_nombre']
    ordering = ['-fecha']

    def get_queryset(self):
        # Anotamos usuario_nombre para permitir ordenamiento por nombre de usuario
        # Mismo patrón que VehiculoViewSet usa para marca_nombre/modelo_nombre
        return LogAuditoria.objects.annotate(
            usuario_nombre=F('usuario__username')
        ).all()
