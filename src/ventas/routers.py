from .views import (
    VentaViewSet, VentaGetViewSet,
    DetalleVentaViewSet, DetalleVentaGetViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('venta', VentaViewSet, basename='venta-api')
router.register('venta-get', VentaGetViewSet, basename='venta-get-api')
router.register('detalle-venta', DetalleVentaViewSet, basename='detalle-venta-api')
router.register('detalle-venta-get', DetalleVentaGetViewSet, basename='detalle-venta-get-api')
