from django.contrib import admin
from .models import Venta, DetalleVenta


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'estado', 'nro_factura', 'is_active', 'created_at']
    list_filter = ['estado', 'is_active']
    search_fields = ['nro_factura', 'cliente__username']
    ordering = ['-created_at']


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'venta', 'producto', 'unidades', 'precio_unitario', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['venta__nro_factura', 'producto__nombre']
    ordering = ['-created_at']
