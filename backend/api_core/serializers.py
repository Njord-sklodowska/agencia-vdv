from rest_framework import serializers
# Importamos todos los modelos que vamos a usar
from .models import InventarioVehiculo, InventarioMarca, SucursalSucursal

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioVehiculo
        fields = '__all__'

# Agregamos estos nuevos para poder usarlos en el Frontend
class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioMarca
        fields = '__all__'

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SucursalSucursal
        fields = '__all__'