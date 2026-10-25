from django.contrib import admin
from .models import Categoria, Marca, Producto, DetalleCompra, Compra, DetalleVenta, Venta, Proveedor, ProductoImagen


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['nombre']
    ordering = ['-created_at']


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'pais_origen', 'is_active', 'created_at']
    list_filter = ['is_active', 'pais_origen']
    search_fields = ['nombre']
    ordering = ['-created_at']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'sku', 'precio_lista', 'stock_total', 'is_active', 'destacado', 'marca', 'categoria']
    list_filter = ['is_active', 'destacado', 'marca', 'categoria']
    search_fields = ['nombre', 'sku']
    ordering = ['-created_at']


@admin.register(ProductoImagen)
class ProductoImagenAdmin(admin.ModelAdmin):
    list_display = ['id', 'producto', 'es_principal', 'is_active', 'created_at']
    list_filter = ['is_active', 'es_principal']
    search_fields = ['producto__nombre']
    ordering = ['-created_at']


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'cuit', 'email', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['nombre', 'cuit', 'email']
    ordering = ['-created_at']


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