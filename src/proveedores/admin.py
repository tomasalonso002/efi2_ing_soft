from django.contrib import admin
from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'cuit', 'email', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['nombre', 'cuit', 'email']
    ordering = ['-created_at']
