from .views import CategoriaGetViewSet, CategoriaViewSet, MarcaGetViewSet, MarcaViewSet, ProveedorViewSet,ProveedorGetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#CATEGORIA
router.register('categoria', CategoriaViewSet, basename='categoria-api')
router.register('categoria-get', CategoriaGetViewSet, basename='categoria-get-api')
#MARCA
router.register('marca', MarcaViewSet, basename='marca-api')
router.register('marca-get', MarcaGetViewSet, basename='marca-get-api')
#PROVEEDOR
router.register('proveedor', ProveedorViewSet, basename='proveedor-api')
router.register('proveedor-get', ProveedorGetViewSet, basename='proveedor-get-api')
#PRODUCTO


#PRODUCTO_IMAGEN


#COMPRA


#DETALLE_COMPRA


#VENTA


#DETALLE VENTA


#