from rest_framework import serializers
from .models import Venta, DetalleVenta


class DetalleVentaSerializer(serializers.ModelSerializer):
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
