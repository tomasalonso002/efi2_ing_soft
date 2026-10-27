from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import AllowAny
from usuarios.permissions import PermissionVendedor
from rest_framework.decorators import action

from .models import Proveedor
from .serializers import ProveedorSerializer


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProveedorSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [PermissionVendedor]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        proveedor = self.get_object()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        proveedor.is_active = False
        proveedor.nombre = f'delete-{proveedor.nombre}-{timestamp}'
        proveedor.cuit = f'delete-{proveedor.cuit}-{timestamp}' if proveedor.cuit else f'delete-{timestamp}'
        proveedor.save()
        return Response(
            {'detail': 'El proveedor se elimino correctamente'},
            status=status.HTTP_200_OK
        )


class ProveedorGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Proveedor.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProveedorSerializer
    permission_classes = [AllowAny]
