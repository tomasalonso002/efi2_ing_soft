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
    total = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = [
            'id', 'cliente', 'estado', 'nro_factura',
            'created_at', 'is_active', 'total'
        ]
        read_only_fields = ['id', 'created_at', 'is_active']

    def get_total(self, obj):
        # Suma (unidades * precio_unitario) de todos los detalles de esta venta
        total = sum(detalle.unidades * detalle.precio_unitario for detalle in obj.detalles.all())
        return total
