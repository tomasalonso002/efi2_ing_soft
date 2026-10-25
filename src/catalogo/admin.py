from django.contrib import admin
from .models import Categoria, Marca, Producto


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