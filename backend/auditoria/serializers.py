from rest_framework import serializers
from .models import LogAuditoria


class LogAuditoriaSerializer(serializers.ModelSerializer):

    usuario_nombre = serializers.CharField(
        source='usuario.username',
        read_only=True
    )

    class Meta:
        model = LogAuditoria
        fields = '__all__'