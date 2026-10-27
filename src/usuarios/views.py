from rest_framework import status, viewsets
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils import timezone
from datetime import timedelta

from rest_framework.permissions import AllowAny
from .permissions import PermissionVendedor, PermissionCliente

from django.contrib.auth.models import Group
from .models import UsuarioPersonalizado,ListaDeseosProductos

from .serializers import UsuarioPublicSerializer,UsuarioSerializer, ListaDeseosGetSerializer, ListaDeseosPostSerializer

#View UsuarioCliente
class UserClienteViewSets(viewsets.ModelViewSet):
    queryset = UsuarioPersonalizado.objects.filter(is_active = True, groups__name = 'Cliente' ).order_by('-id')
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [AllowAny]
        else:
            permission_classes = [PermissionCliente]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = serializer.save()
        grupo = Group.objects.get(name='Cliente')
        user.groups.add(grupo)
   
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

#GET ReadOnly UsuarioCliente
class UserClienteGetViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = UsuarioPersonalizado.objects.filter(is_active = True, groups__name = 'Cliente' ).order_by('-id')
    serializer_class = UsuarioPublicSerializer
    permission_classes=[PermissionVendedor]


#View UsuarioVendedor
class UserVendedorViewSets(viewsets.ModelViewSet):
    queryset = UsuarioPersonalizado.objects.filter(is_active = True,  groups__name = 'Vendedor' ).order_by('-id')
    serializer_class = UsuarioSerializer
    permission_classes=[PermissionVendedor]

    def perform_create(self, serializer):
        user = serializer.save()
        grupo = Group.objects.get(name='Vendedor')
        user.groups.add(grupo)
   
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
            {'detail':'El vendedor se elimino correctamente'},
            status= status.HTTP_200_OK
        )


#GET ReadOnly UsuarioVendedor
class UserVendedorGetViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = UsuarioPersonalizado.objects.filter(is_active = True, groups__name = 'Vendedor' )
    serializer_class = UsuarioPublicSerializer
    permission_classes=[PermissionVendedor]


#POST Lista de desos
class ListaDeseosProductosPostViewSets(viewsets.ModelViewSet):
    queryset = ListaDeseosProductos.objects.filter(is_active = True)
    serializer_class = ListaDeseosPostSerializer
    permission_classes = [PermissionCliente]

    def perform_create(self, serializer):
        serializer.save(usuario = self.request.user)

    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        producto = self.get_object()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        producto.is_active = False
        producto.nombre = f'delete-{producto}-{timestamp}'
        producto.save()
        return Response(
            {'detail':'Se quito el producto de lista de deseos'},
            status= status.HTTP_200_OK
        )

class ListaDeseosProductosViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = ListaDeseosProductos.objects.filter(is_active=True).select_related('usuario', 'producto')
    serializer_class = ListaDeseosGetSerializer
    permission_classes = [PermissionCliente]


#RENDERIZADO DE TEMPLETE
def inicio(request):
    return render(
        request,
        'usuarios/inicio.html',
    )