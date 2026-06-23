from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Importamos los nuevos ViewSets que creamos
from .views import VehiculoViewSet, MarcaViewSet, SucursalViewSet 

# 1. Creamos el router
router = DefaultRouter()

# 2. Registramos las rutas
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculo')
router.register(r'marcas', MarcaViewSet, basename='marca')       # Nueva ruta
router.register(r'sucursales', SucursalViewSet, basename='sucursal') # Nueva ruta

# 3. urlpatterns es el portero que conecta todo
urlpatterns = [
    path('', include(router.urls)),
]