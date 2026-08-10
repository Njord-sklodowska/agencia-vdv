from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import LogAuditoria
from .serializers import LogAuditoriaSerializer


class LogAuditoriaListView(generics.ListAPIView):

    queryset = LogAuditoria.objects.all()
    serializer_class = LogAuditoriaSerializer
    permission_classes = [IsAuthenticated]