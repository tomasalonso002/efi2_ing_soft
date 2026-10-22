from .views import CategoriaViewSet, MarcaViewSet, ProductoViewSet, ProductoImagenViewSet, EspecificacionViewSet, VarianteViewSet, CompatibilidadViewSet, EtiquetaViewSet, ProductoEtiquetaViewSet, ProveedorViewSet, CompraViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('categorias', CategoriaViewSet, basename='categoria-api')
router.register('marcas', MarcaViewSet, basename='marca')
router.register('productos', ProductoViewSet, basename='producto')
router.register('producto-imagenes', ProductoImagenViewSet, basename='producto-imagen')
router.register('especificaciones', EspecificacionViewSet, basename='especificacion')
router.register('variantes', VarianteViewSet, basename='variante')
router.register('compatibilidades', CompatibilidadViewSet, basename='compatibilidad')
router.register('etiquetas', EtiquetaViewSet, basename='etiqueta')
router.register('producto-etiquetas', ProductoEtiquetaViewSet, basename='producto-etiqueta')
router.register('proveedores', ProveedorViewSet, basename='proveedor')
router.register('compras', CompraViewSet, basename='compra')
