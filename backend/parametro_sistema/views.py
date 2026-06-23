from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import ParametroSistema
from .serializers import ParametroSistemaSerializer


class ParametroSistemaViewSet(ModelViewSet):
    queryset = ParametroSistema.objects.all()
    serializer_class = ParametroSistemaSerializer
    permission_classes = [IsAuthenticated]