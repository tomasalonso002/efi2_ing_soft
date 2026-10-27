from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.utils import timezone

from rest_framework.permissions import AllowAny
from usuarios.permissions import PermissionVendedor, PermissionCliente

from rest_framework.decorators import action

from .models import (Categoria, Marca, Producto)
from .serializers import (CategoriaSerializer, MarcaSerializer, ProductoSerializer, ProductoListSerializer,)

#CATEGORIA

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.filter(is_active=True).order_by('nombre')
    serializer_class = CategoriaSerializer

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


#PRODUCTOS

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['marca', 'categoria', 'destacado', 'is_active']
    search_fields = ['nombre', 'sku', 'descripcion_corta']
    ordering_fields = ['precio_lista', 'precio_oferta', 'stock_total', 'created_at']
    ordering = ['-created_at']

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
