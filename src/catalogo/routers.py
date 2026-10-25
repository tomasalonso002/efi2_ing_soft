from .views import (CategoriaGetViewSet, CategoriaViewSet, MarcaGetViewSet, MarcaViewSet, ProveedorViewSet,ProveedorGetViewSet, ProductoViewSet, ProductoGetViewSet, CompraViewSet, CompraGetViewSet, DetalleCompraViewSet, DetalleCompraGetViewSet)
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
router.register('producto', ProductoViewSet, basename='producto-api')
router.register('producto-get', ProductoGetViewSet, basename='producto-get-api')


#PRODUCTO_IMAGEN

#COMPRA
router.register('compra', CompraViewSet, basename='compra-api')
router.register('compra-get', CompraGetViewSet, basename='compra-get-api')

#DETALLE_COMPRA
router.register('detalle-compra', DetalleCompraViewSet, basename='detalle-compra-api')
router.register('detalle-compra-get', DetalleCompraGetViewSet, basename='detalle-compra-get-api')


#VENTA


#DETALLE VENTA


#