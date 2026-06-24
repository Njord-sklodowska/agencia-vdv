from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import CharFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Case, When, Value, F
from django.db.models.functions import Concat
from django.db import models
from config.pagination import StandardResultsSetPagination
from config.mixins import AuditMixin
from rest_framework.response import Response
from rest_framework import status

from .models import Cliente
from .serializers import ClienteSerializer


class ClienteFilter(FilterSet):
    telefono = CharFilter(method='filter_telefono')

    class Meta:
        model = Cliente
        fields = ['tipo_persona', 'estado']

    def filter_telefono(self, queryset, name, value):
        if not value:
            return queryset
        # Limpiar el valor buscado (quitar guiones, espacios, paréntesis, puntos)
        import re
        cleaned_value = re.sub(r'[^\d]', '', value)
        if not cleaned_value:
            return queryset
        # Buscar en ambos campos de teléfono usando icontains
        from django.db.models import Q
        return queryset.filter(
            Q(telefono__icontains=cleaned_value) |
            Q(telefono_alternativo__icontains=cleaned_value)
        )


class ClienteViewSet(AuditMixin, viewsets.ModelViewSet):
    modulo_name = "Clientes"
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    # Configuración de Filtros
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ClienteFilter
    search_fields = ['dni_cuit', 'cuil', 'nombre', 'apellido', 'razon_social', 'nombre_fantasia', 'telefono']
    ordering_fields = ['fecha_alta', 'full_name', 'dni_cuit']

    def get_queryset(self):
        # 1. Creamos el campo virtual para el ordenamiento unificado
        queryset = Cliente.objects.annotate(
            full_name=Case(
                When(tipo_persona='fisica', then=Concat('apellido', Value(', '), 'nombre')),
                default=F('razon_social'),
                output_field=models.CharField(),
            )
        )
        
        # 2. Manejo MANUAL y FORZADO del ordenamiento
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            # Aplicamos el ordenamiento directamente al queryset de la DB
            queryset = queryset.order_by(ordering)
        else:
            # Orden predeterminado
            queryset = queryset.order_by('-fecha_alta')

        return queryset

    def perform_destroy(self, instance):
        # Implementación de Borrado Lógico
        instance.estado = 'inactivo'
        instance.save()
        # Registramos la acción en auditoría a través del Mixin
        # El Mixin espera que llamemos a _log_action manualmente si sobrescribimos perform_destroy
        # ya que el Mixin original llamaba a instance.delete()
        desc = f"Se desactivó el cliente {instance.full_name if hasattr(instance, 'full_name') else instance.username} (ID: {instance.pk})"
        self._log_action(instance, 'ELIMINAR', desc)
