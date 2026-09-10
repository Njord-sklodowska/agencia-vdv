from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoDocumentoViewSet, GestorViewSet, DocumentacionVehiculoViewSet

router = DefaultRouter()
router.register(r'tipos-documento', TipoDocumentoViewSet, basename='tipodocumento')
router.register(r'gestores', GestorViewSet, basename='gestor')
router.register(r'documentacion-vehiculo', DocumentacionVehiculoViewSet, basename='documentacionvehiculo')

urlpatterns = [
    path('', include(router.urls)),
]