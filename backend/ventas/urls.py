
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OperacionVentaViewSet, FormaPagoViewSet, AnticipoViewSet

router = DefaultRouter()
router.register(r'operaciones', OperacionVentaViewSet, basename='operacion')
router.register(r'anticipos', AnticipoViewSet, basename='anticipo')

urlpatterns = [
    path('', include(router.urls)),
    # URLs anidadas para formas de pago
    path('operaciones/<int:operacion_pk>/formas-pago/', FormaPagoViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='operacion-formaspago-list'),
    path('operaciones/<int:operacion_pk>/formas-pago/<int:pk>/', FormaPagoViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    }), name='operacion-formaspago-detail'),
]