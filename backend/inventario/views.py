

from rest_framework import viewsets
from rest_framework.response import Response
from .models import Marca, Modelo
from . import MarcaSerializer, ModeloSerializer

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer