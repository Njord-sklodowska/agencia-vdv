from config.serializers import ValidatedModelSerializer
from .models import Sucursal


class SucursalSerializer(ValidatedModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'