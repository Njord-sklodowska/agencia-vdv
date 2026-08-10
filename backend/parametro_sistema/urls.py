from rest_framework.routers import DefaultRouter
from .views import ParametroSistemaViewSet

router = DefaultRouter()
router.register(
    r'parametros-sistema',
    ParametroSistemaViewSet,
    basename='parametros-sistema'
)

urlpatterns = router.urls