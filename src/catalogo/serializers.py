from rest_framework import serializers
from .models import (
    Categoria,
    Marca,
    Producto,
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

#CATEGORIA
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'descripcion', 'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'created_at','is_active']


#PRODUCTO
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion_corta', 'descripcion_larga',
            'sku', 'precio_lista', 'precio_oferta',
            'imagen_url',
            'stock_total', 'is_active', 'destacado',
            'marca', 'categoria',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'is_active']

class ProductoListSerializer(ProductoSerializer):
    marca = MarcaSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    
    class Meta(ProductoSerializer.Meta):
        fields = ProductoSerializer.Meta.fields + [
            'marca', 'categoria',
        ]