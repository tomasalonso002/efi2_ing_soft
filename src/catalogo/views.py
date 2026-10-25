from rest_framework import viewsets,status
from rest_framework.response import Response


from django.utils import timezone
from datetime import timedelta


from rest_framework.permissions import AllowAny
from usuarios.permissions import PermissionVendedor, PermissionCliente

from rest_framework.decorators import action

from .models import (Categoria,Marca,Producto,ProductoImagen,Proveedor,Compra,DetalleCompra)
from .serializers import (CategoriaSerializer,MarcaSerializer,ProductoSerializer,ProductoListSerializer,ProductoImagenSerializer,ProveedorSerializer,CompraSerializer,DetalleCompraSerializer,)

#CATEGORIA

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.filter(is_active=True).order_by('nombre')
    serializer_class = CategoriaSerializer

    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [PermissionVendedor]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        categoria = self.get_object()
        categoria.is_active = False
        categoria.save()
        return Response(
            {'detail':'La categoria se elimino correctamente'},
            status= status.HTTP_200_OK
        )

class CategoriaGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.filter(is_active=True).order_by('nombre')
    serializer_class = CategoriaSerializer

#MARCAS

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.filter(is_active=True).order_by('nombre')
    serializer_class = MarcaSerializer

    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [PermissionVendedor]

        return [permission() for permission in permission_classes]
    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        marca = self.get_object()
        marca.is_active = False
        marca.save()
        return Response(
            {'detail':'La marca se elimino correctamente'},
            status= status.HTTP_200_OK
        )

class MarcaGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Marca.objects.filter(is_active=True).order_by('nombre')
    serializer_class = MarcaSerializer


#PROVEEDOR
class ProveedorViewSet(viewsets.ModelViewSet):
    queryset= Proveedor.objects.filter(is_active = True)
    serializer_class= ProveedorSerializer
    permission_classes = [PermissionVendedor]

    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        proveedor = self.get_object()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        proveedor.is_active = False
        proveedor.nombre = f'delete-{proveedor.nombre}-{timestamp}'
        proveedor.cuit = f'delete-{proveedor.cuit}-{timestamp}'
        proveedor.save()
        return Response(
            {'detail':'El proveedor se elimino correctamente'},
            status= status.HTTP_200_OK
        )

class ProveedorGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Proveedor.objects.filter(is_active = True)
    serializer_class = ProveedorSerializer
    permission_classes = [PermissionVendedor]

#PRODUCTOS

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProductoSerializer

    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [PermissionVendedor]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        producto = self.get_object()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        producto.is_active = False
        producto.nombre = f'delete-{producto.nombre}-{timestamp}'
        producto.sku = f'delete-{producto.sku}-{timestamp}'
        producto.save()
        return Response(
            {'detail':'El producto se elimino correctamente'},
            status=status.HTTP_200_OK
        )

class ProductoGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.filter(is_active=True).select_related('marca', 'categoria').order_by('-created_at')
    serializer_class = ProductoListSerializer
    permission_classes = [AllowAny]

#PRODUCTO_IMG

#COMPRA

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = CompraSerializer

    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [PermissionVendedor]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        compra = self.get_object()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        compra.is_active = False
        compra.nro_factura = f'delete-{compra.nro_factura}-{timestamp}' if compra.nro_factura else f'delete-{timestamp}'
        compra.save()
        return Response(
            {'detail':'La compra se elimino correctamente'},
            status=status.HTTP_200_OK
        )

class CompraGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Compra.objects.filter(is_active=True).select_related('proveedor').order_by('-created_at')
    serializer_class = CompraSerializer
    permission_classes = [AllowAny]

#DETALLE_COMPRA

class DetalleCompraViewSet(viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = DetalleCompraSerializer

    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [PermissionVendedor]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        detalle = self.get_object()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        detalle.is_active = False
        detalle.save()
        return Response(
            {'detail':'El detalle de compra se elimino correctamente'},
            status=status.HTTP_200_OK
        )

class DetalleCompraGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DetalleCompra.objects.filter(is_active=True).select_related('compra', 'producto').order_by('-created_at')
    serializer_class = DetalleCompraSerializer
    permission_classes = [AllowAny]

#VENTA

#DETALLE_VENTA
