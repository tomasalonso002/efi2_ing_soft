from rest_framework import viewsets
from .models import (
    Categoria,
    Marca,
    Producto,
    ProductoImagen,
    Proveedor,
    Compra,
)
from .serializers import (
    CategoriaSerializer,
    MarcaSerializer,
    ProductoSerializer,
    ProductoListSerializer,
    ProductoImagenSerializer,
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


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
