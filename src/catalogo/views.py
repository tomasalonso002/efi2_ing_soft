from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
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

from usuarios.permissions import PermissionVendedor, PermissionCliente

#CATEGORIA

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.filter(is_active = True).order_by('-id')
    serializer_class = CategoriaSerializer
    permission_classes = [PermissionVendedor]

    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        user = self.get_object()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        user.is_active = False
        user.username = f'delete-{user.username}-{timestamp}'
        user.email = f'delete-{user.email}-{timestamp}'
        user.dni = f'delete-{user.dni}-{timestamp}'
        user.save()
        return Response(
            {'detail':'El usuario se elimino correctamente'},
            status= status.HTTP_200_OK
        )

#MARCAS

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.filter(is_active = True).order_by('-id')
    serializer_class = MarcaSerializer
    permission_classes = [PermissionVendedor]


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
