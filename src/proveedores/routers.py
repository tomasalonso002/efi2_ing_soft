from .views import ProveedorViewSet, ProveedorGetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('proveedor', ProveedorViewSet, basename='proveedor-api')
router.register('proveedor-get', ProveedorGetViewSet, basename='proveedor-get-api')
