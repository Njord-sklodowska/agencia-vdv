from rest_framework import viewsets
# Importamos todos los modelos y serializadores necesarios
from .models import InventarioVehiculo, InventarioMarca, SucursalSucursal
from .serializers import VehiculoSerializer, MarcaSerializer, SucursalSerializer

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = InventarioVehiculo.objects.all()
    serializer_class = VehiculoSerializer

# Agregamos las nuevas clases de control
class MarcaViewSet(viewsets.ModelViewSet):
    queryset = InventarioMarca.objects.all()
    serializer_class = MarcaSerializer

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = SucursalSucursal.objects.all()
    serializer_class = SucursalSerializer