from rest_framework import serializers
from .models import Proveedor


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = [
            'id', 'nombre', 'cuit', 'email', 'telefono', 'direccion',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'is_active']
