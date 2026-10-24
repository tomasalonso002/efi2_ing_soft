from rest_framework import serializers
from .models import (
    Categoria,
    Marca,
    Producto,
    ProductoImagen,
    Proveedor,
    Compra,
    DetalleCompra,
    Venta,
    DetalleVenta

)
#MARCA
class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = [
            'id', 'nombre', 'logo', 'descripcion',
            'pais_origen', 'is_active', 'created_at',
        ]
        read_only_fields = ['id','is_active','created_at']

#PROVEEDOR
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = [
            'id', 'nombre', 'cuit', 'email', 'telefono', 'direccion',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'is_active', 'created_at']

#CATEGORIA
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'descripcion', 'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'created_at','is_active']


#PRODUCTO
class ProductoImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoImagen
        fields = [
            'id', 'producto', 'imagen_url', 'alt_text', 'orden',
            'es_principal', 'created_at','is_active'
        ]
        read_only_fields = ['id', 'created_at','is_active']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion_corta', 'descripcion_larga',
            'sku', 'precio_lista', 'precio_oferta',
            'stock_total', 'stock_reservado', 'is_active', 'destacado',
            'marca', 'categoria',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at','is_active']

class ProductoListSerializer(ProductoSerializer):
    marca = MarcaSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    imagenes = ProductoImagenSerializer(many=True, read_only=True)
    
    class Meta(ProductoSerializer.Meta):
        fields = ProductoSerializer.Meta.fields + [
            'marca', 'categoria', 'imagenes', 'especificaciones', 'variantes',
        ]

#COMPRA
class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = [
            'id', 'proveedor', 'total', 'estado', 'nro_factura',
            'created_at','is_active'
        ]
        read_only_fields = ['id', 'created_at','is_active']


class DetalleCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        field = [
            'id','compra','producto','unidades','precio','created_at'
        ]
        read_only_fields = ['id', 'created_at','is_active']




