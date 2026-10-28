from django.contrib import admin
from .models import UsuarioPersonalizado, ListaDeseosProductos


@admin.register(UsuarioPersonalizado)
class UsuarioPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'dni', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'dni', 'telefono']
    ordering = ['-id']


@admin.register(ListaDeseosProductos)
class ListaDeseosProductosAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'producto', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['usuario__username', 'producto__nombre']
    ordering = ['-created_at']
