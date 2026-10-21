from rest_framework import viewsets
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
from .serializers import (
    CategoriaSerializer,
    MarcaSerializer,
    ProductoSerializer,
    ProductoListSerializer,
    ProductoImagenSerializer,
    EspecificacionSerializer,
    VarianteSerializer,
    CompatibilidadSerializer,
    EtiquetaSerializer,
    ProductoEtiquetaSerializer,
    ProveedorSerializer,
    CompraSerializer,
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductoListSerializer
        return ProductoSerializer


class ProductoImagenViewSet(viewsets.ModelViewSet):
    queryset = ProductoImagen.objects.all()
    serializer_class = ProductoImagenSerializer


class EspecificacionViewSet(viewsets.ModelViewSet):
    queryset = Especificacion.objects.all()
    serializer_class = EspecificacionSerializer


class VarianteViewSet(viewsets.ModelViewSet):
    queryset = Variante.objects.all()
    serializer_class = VarianteSerializer


class CompatibilidadViewSet(viewsets.ModelViewSet):
    queryset = Compatibilidad.objects.all()
    serializer_class = CompatibilidadSerializer


class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer


class ProductoEtiquetaViewSet(viewsets.ModelViewSet):
    queryset = ProductoEtiqueta.objects.all()
    serializer_class = ProductoEtiquetaSerializer


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
