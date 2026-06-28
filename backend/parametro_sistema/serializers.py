from config.serializers import ValidatedModelSerializer
from .models import ParametroSistema


class ParametroSistemaSerializer(ValidatedModelSerializer):

    class Meta:
        model = ParametroSistema
        fields = '__all__'
