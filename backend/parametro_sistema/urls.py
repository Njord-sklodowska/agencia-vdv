from rest_framework.routers import DefaultRouter
from .views import ParametroSistemaViewSet

router = DefaultRouter()
router.register(
    r'parametros',
    ParametroSistemaViewSet,
    basename='parametros'
)

urlpatterns = router.urls