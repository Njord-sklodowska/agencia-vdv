from rest_framework import serializers
from config.serializers import ValidatedModelSerializer
from .models import Cliente

class ClienteSerializer(ValidatedModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Cliente
        fields = '__all__'
