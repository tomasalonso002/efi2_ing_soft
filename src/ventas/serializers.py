from rest_framework import serializers
from .models import Venta, DetalleVenta
from catalogo.serializers import ProductoListSerializer
from usuarios.serializers import UsuarioPublicSerializer


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = ProductoListSerializer(read_only=True)

    class Meta:
        model = DetalleVenta
        fields = [
            'id', 'venta', 'producto', 'unidades', 'precio_unitario',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'is_active']


class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = [
            'id', 'cliente', 'estado', 'nro_factura',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'is_active']


class VentaGetSerializer(serializers.ModelSerializer):
    cliente = UsuarioPublicSerializer(read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id', 'cliente', 'estado', 'nro_factura',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'is_active']
