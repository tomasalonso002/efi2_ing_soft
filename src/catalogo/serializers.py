from rest_framework import serializers
from .models import (
    Categoria,
    Marca,
    Producto,
    ProductoImagen,
    Proveedor,
    Compra,
    DetalleCompra
)


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = [
            'id', 'nombre', 'logo', 'descripcion',
            'pais_origen', 'is_active', 'created_at',
        ]
        read_only_fields = ['id','is_active','created_at']

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = [
            'id', 'nombre', 'cuit', 'email', 'telefono', 'direccion',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'is_active', 'created_at', 'updated_at']

class ProductoImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoImagen
        fields = [
            'id', 'producto', 'imagen_url', 'alt_text', 'orden',
            'es_principal', 'created_at','is_active'
        ]
        read_only_fields = ['id', 'created_at','is_active']

#class VarianteSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Variante
#        fields = [
#            'id', 'producto', 'sku_variante', 'nombre', 'precio_adicional',
#            'stock', 'activa', 'atributos', 'created_at', 'updated_at',
#        ]
#        read_only_fields = ['id', 'created_at', 'updated_at']

#    def validate_stock(self, value):
#        if value < 0:
#            raise serializers.ValidationError('El stock no puede ser negativo.')
#        return value

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



class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'descripcion', 'is_active', 'created_at',
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
