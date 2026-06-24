from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sucursal
from .serializers import SucursalSerializer
from config.pagination import StandardResultsSetPagination


class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['estado', 'provincia', 'ciudad']
    search_fields = ['nombre', 'direccion', 'ciudad', 'provincia']
    ordering_fields = ['nombre', 'ciudad', 'provincia', 'estado']
