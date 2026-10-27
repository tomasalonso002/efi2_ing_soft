from .views import (
    CompraViewSet, CompraGetViewSet, CompraListGetViewSet,
    DetalleCompraViewSet, DetalleCompraGetViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('compra', CompraViewSet, basename='compra-api')
router.register('compra-get', CompraGetViewSet, basename='compra-get-api')
router.register('compra-list', CompraListGetViewSet, basename='compra-list-api')
router.register('detalle-compra', DetalleCompraViewSet, basename='detalle-compra-api')
router.register('detalle-compra-get', DetalleCompraGetViewSet, basename='detalle-compra-get-api')
