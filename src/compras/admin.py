from django.contrib import admin
from .models import Compra, DetalleCompra


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'proveedor', 'estado', 'nro_factura', 'total', 'is_active', 'created_at']
    list_filter = ['estado', 'is_active']
    search_fields = ['nro_factura', 'proveedor__nombre']
    ordering = ['-created_at']


@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'compra', 'producto', 'unidades', 'precio', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['compra__nro_factura', 'producto__nombre']
    ordering = ['-created_at']
