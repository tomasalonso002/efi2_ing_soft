from .views import UserClienteViewSets, UserVendedorViewSets, UserClienteGetViewSets, UserVendedorGetViewSets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('cliente', UserClienteViewSets, basename='user-cliente-api')
router.register('cliente-get', UserClienteViewSets, basename='user-cliente-get-api')
router.register('vendedor', UserVendedorViewSets, basename='user-vendedor-api')
router.register('vendedor-get', UserVendedorViewSets, basename='user-vendedor-get-api')
