from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils import timezone
from datetime import timedelta


from .permissions import PermissionVendedor, PermissionUser

from django.contrib.auth.models import Group
from .models import UsuarioPersonalizado

from .serializers import UsuarioPublicSerializer,UsuarioSerializer

#View UsuarioCliente
class UserClienteViewSets(viewsets.ModelViewSet):
    queryset = UsuarioPersonalizado.objects.filter(is_active = True)
    serializer_class = UsuarioSerializer

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
        return self.response(
            {'detail':'El usuario se elimino correctamente'},
            status= status.HTTP_200_OK
        )

#GET ReadOnly UsuarioCliente
class UserClienteGetViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = UsuarioPersonalizado.objects.filter(is_active = True, groups__name = 'Cliente' )
    serializer_class = UsuarioPublicSerializer
    permission_classes=[PermissionVendedor]

#View UsuarioVendedor
class UserVendedorViewSets(viewsets.ModelViewSet):
    queryset = UsuarioPersonalizado.objects.filter(is_active = True)
    serializer_class = UsuarioSerializer

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
        return self.response(
            {'detail':'El vendedor se elimino correctamente'},
            status= status.HTTP_200_OK
        )

#GET ReadOnly UsuarioVendedor
class UserVendedorGetViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = UsuarioPersonalizado.objects.filter(is_active = True, groups__name = 'Vendedor' )
    serializer_class = UsuarioPublicSerializer
    permission_classes=[PermissionVendedor]