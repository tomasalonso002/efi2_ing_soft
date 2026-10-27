from .views import (CategoriaGetViewSet, CategoriaViewSet, MarcaGetViewSet, MarcaViewSet, ProductoViewSet, ProductoGetViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#CATEGORIA
router.register('categoria', CategoriaViewSet, basename='categoria-api')
router.register('categoria-get', CategoriaGetViewSet, basename='categoria-get-api')
#MARCA
router.register('marca', MarcaViewSet, basename='marca-api')
router.register('marca-get', MarcaGetViewSet, basename='marca-get-api')
#PRODUCTO
router.register('producto', ProductoViewSet, basename='producto-api')
router.register('producto-get', ProductoGetViewSet, basename='producto-get-api')
