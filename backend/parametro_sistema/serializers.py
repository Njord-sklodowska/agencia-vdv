from rest_framework import serializers
from .models import ParametroSistema


class ParametroSistemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParametroSistema
        fields = '__all__'