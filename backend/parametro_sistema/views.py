from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.exceptions import PermissionDenied
from config.pagination import StandardResultsSetPagination
from config.mixins import AuditMixin

from .models import ParametroSistema
from .serializers import ParametroSistemaSerializer


class ParametroSistemaViewSet(AuditMixin, ModelViewSet):
    modulo_name = "Administración"
    queryset = ParametroSistema.objects.all()
    serializer_class = ParametroSistemaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter, SearchFilter]
    
    search_fields = ['nombre_parametro', 'descripcion']
    ordering_fields = ['nombre_parametro', 'fecha_alta']

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("Solo el superusuario puede eliminar parámetros del sistema.")
        return super().destroy(request, *args, **kwargs)
