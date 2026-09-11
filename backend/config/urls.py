from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # APPS DEL PROYECTO
    path('api/usuario/', include('usuario.urls')),
    path('api/sucursal/', include('sucursal.urls')),
    path('api/inventario/', include('inventario.urls')),
    path('api/parametro_sistema/', include('parametro_sistema.urls')),
    path('api/clientes/', include('clientes.urls')),
    path('api/auditoria/', include('auditoria.urls')),
    path('api/ventas/', include('ventas.urls')),
    path('api/documentacion/', include('documentacion.urls')),
    # JWT AUTH
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # redirect opcional al admin
    path('', lambda request: redirect('admin:index')),
]

# MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)