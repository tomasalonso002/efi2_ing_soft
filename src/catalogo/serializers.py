from rest_framework import serializers
from .models import (
    Categoria,
    Marca,
    Producto,
    ProductoImagen,
    Especificacion,
    Variante,
    Compatibilidad,
    Etiqueta,
    ProductoEtiqueta,
    Proveedor,
    Compra,
)


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = [
            'id', 'nombre', 'slug', 'logo_url', 'descripcion',
            'pais_origen', 'activa', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = ['id', 'nombre', 'slug', 'color_hex', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = [
            'id', 'nombre', 'cuit', 'email', 'telefono', 'direccion',
            'activo', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductoImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoImagen
        fields = [
            'id', 'producto', 'imagen_url', 'alt_text', 'orden',
            'es_principal', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        es_principal = data.get('es_principal', False)
        producto = data.get('producto') or getattr(self.instance, 'producto', None)
        if es_principal and producto:
            qs = ProductoImagen.objects.filter(producto=producto, es_principal=True)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    'Ya existe una imagen principal para este producto.'
                )
        return data


class EspecificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especificacion
        fields = [
            'id', 'producto', 'nombre', 'valor', 'tipo', 'unidad', 'orden',
        ]
        read_only_fields = ['id']


class VarianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variante
        fields = [
            'id', 'producto', 'sku_variante', 'nombre', 'precio_adicional',
            'stock', 'activa', 'atributos', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock no puede ser negativo.')
        return value


class CompatibilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compatibilidad
        fields = [
            'id', 'producto', 'producto_compatible', 'tipo_compatibilidad',
            'notas', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        producto = data.get('producto') or getattr(self.instance, 'producto', None)
        producto_compatible = data.get('producto_compatible') or getattr(
            self.instance, 'producto_compatible', None
        )
        if producto and producto_compatible and producto == producto_compatible:
            raise serializers.ValidationError(
                'Un producto no puede ser compatible consigo mismo.'
            )
        return data


class ProductoEtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoEtiqueta
        fields = ['id', 'producto', 'etiqueta', 'created_at']
        read_only_fields = ['id', 'created_at']


class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = [
            'id', 'proveedor', 'fecha_compra', 'total', 'estado', 'nro_factura',
            'created_at',
        ]
        read_only_fields = ['id', 'fecha_compra', 'created_at']

    def validate_total(self, value):
        if value < 0:
            raise serializers.ValidationError('El total no puede ser negativo.')
        return value


class CategoriaSerializer(serializers.ModelSerializer):
    subcategorias = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'slug', 'descripcion', 'imagen_url',
            'categoria_padre', 'orden', 'activa', 'created_at', 'subcategorias',
        ]
        read_only_fields = ['id', 'created_at']

    def get_subcategorias(self, obj):
        request = self.context.get('request')
        if request and request.parser_context.get('kwargs', {}).get('pk'):
            return []
        subcats = obj.subcategorias.all()
        return CategoriaSerializer(subcats, many=True, context=self.context).data


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'slug', 'descripcion_corta', 'descripcion_larga',
            'sku', 'precio_lista', 'precio_oferta', 'iva_porcentaje',
            'stock_total', 'stock_reservado', 'activo', 'destacado',
            'fecha_lanzamiento', 'marca', 'categoria',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        precio_lista = data.get('precio_lista') or getattr(
            self.instance, 'precio_lista', None
        )
        precio_oferta = data.get('precio_oferta')
        if precio_oferta is not None and precio_lista is not None:
            if precio_oferta > precio_lista:
                raise serializers.ValidationError(
                    {'precio_oferta': 'El precio de oferta no puede ser mayor al precio de lista.'}
                )
        return data


class ProductoListSerializer(ProductoSerializer):
    marca = MarcaSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    imagenes = ProductoImagenSerializer(many=True, read_only=True)
    especificaciones = EspecificacionSerializer(many=True, read_only=True)
    variantes = VarianteSerializer(many=True, read_only=True)

    class Meta(ProductoSerializer.Meta):
        fields = ProductoSerializer.Meta.fields + [
            'marca', 'categoria', 'imagenes', 'especificaciones', 'variantes',
        ]
