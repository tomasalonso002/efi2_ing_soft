from .views import CategoriaViewSet, MarcaViewSet, ProductoViewSet, ProductoImagenViewSet,ProveedorViewSet, CompraViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('categorias', CategoriaViewSet, basename='categoria-api')
router.register('marcas', MarcaViewSet, basename='marca')
router.register('productos', ProductoViewSet, basename='producto')
router.register('producto-imagenes', ProductoImagenViewSet, basename='producto-imagen')
router.register('proveedores', ProveedorViewSet, basename='proveedor')
router.register('compras', CompraViewSet, basename='compra')
