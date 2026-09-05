
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ( OperacionVentaViewSet, FormaPagoViewSet, AnticipoViewSet, TituloCreditoViewSet, RegistroCobroViewSet, EntidadFinancieraViewSet, FinanciamientoExternoViewSet,CreditoInternoViewSet, CuotaCreditoViewSet)


router = DefaultRouter()
router.register(r'operaciones', OperacionVentaViewSet, basename='operacion')
router.register(r'anticipos', AnticipoViewSet, basename='anticipo')
router.register(r'titulos', TituloCreditoViewSet, basename='titulo')     
router.register(r'cobros', RegistroCobroViewSet, basename='cobro')
router.register(r'entidades-financieras', EntidadFinancieraViewSet, basename='entidad-financiera')
router.register(r'financiamientos-externos', FinanciamientoExternoViewSet, basename='financiamiento-externo')
router.register(r'creditos-internos', CreditoInternoViewSet, basename='credito-interno')   

urlpatterns = [
    path('', include(router.urls)),
    path('operaciones/<int:operacion_pk>/formas-pago/', FormaPagoViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='operacion-formaspago-list'),
    path('operaciones/<int:operacion_pk>/formas-pago/<int:pk>/', FormaPagoViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    }), name='operacion-formaspago-detail'),
      path('creditos-internos/<int:credito_pk>/cuotas/', CuotaCreditoViewSet.as_view({
        'get': 'list'
    }), name='credito-cuotas-list'),
    path('creditos-internos/<int:credito_pk>/cuotas/<int:pk>/', CuotaCreditoViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update'
    }), name='credito-cuotas-detail'),
    path('creditos-internos/<int:credito_pk>/cuotas/<int:pk>/registrar_pago/', CuotaCreditoViewSet.as_view({
        'post': 'registrar_pago'
    }), name='credito-cuotas-registrar-pago'),

]
     
