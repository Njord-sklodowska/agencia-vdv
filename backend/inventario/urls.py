

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MarcaViewSet, ModeloViewSet, VehiculoViewSet,
    FotografiaVehiculoViewSet, TallerViewSet,
    VehiculoUsadoViewSet, TrasladoVehiculoViewSet
)

router = DefaultRouter()
router.register(r'marcas', MarcaViewSet, basename='marca')
router.register(r'modelos', ModeloViewSet, basename='modelo')
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculo')
router.register(r'talleres', TallerViewSet, basename='taller')
router.register(r'vehiculos-usados', VehiculoUsadoViewSet, basename='vehiculo-usado')
router.register(r'traslados', TrasladoVehiculoViewSet, basename='traslado')

urlpatterns = [
    path('', include(router.urls)),
    # URLs anidadas para fotos de un vehículo específico
    path('vehiculos/<int:vehiculo_pk>/fotos/', FotografiaVehiculoViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='vehiculo-fotos-list'),
    path('vehiculos/<int:vehiculo_pk>/fotos/<int:pk>/', FotografiaVehiculoViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    }), name='vehiculo-fotos-detail'),
]