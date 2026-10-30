from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group
from .models import UsuarioPersonalizado, ListaDeseosProductos
from catalogo.serializers import ProductoListSerializer
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 1. Si es superusuario, siempre es admin
        if user.is_superuser:
            token['role'] = 'admin'
        else:
            # 2. Si no, buscamos en los grupos y forzamos minúsculas
            groups = user.groups.all()
            token['role'] = groups.first().name.lower() if groups else ''

        return token


#Serializer GET usuario
class UsuarioPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPersonalizado
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'telefono',
            'dni',
            'email',
            'groups'
        ]

#Serializer POST usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPersonalizado
        fields = [
            'id', 'username', 'last_name', 'first_name',
            'password', 'telefono', 'email', 'dni',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # 1. Limpiamos strings vacíos para que no choquen con las validaciones de la DB
        if validated_data.get('dni') == '':
            validated_data['dni'] = None
        if validated_data.get('telefono') == '':
            validated_data['telefono'] = None
        if validated_data.get('email') == '':
            validated_data['email'] = None

        try:
            # 2. Creamos el usuario
            usuario = UsuarioPersonalizado.objects.create_user(**validated_data)

            # 3. Le asignamos el grupo 'Cliente' (si no existe, lo crea)
            grupo_cliente, _ = Group.objects.get_or_create(name='Cliente')
            usuario.groups.add(grupo_cliente)

            return usuario
        except IntegrityError:
            # Si el username o DNI ya existen, devolvemos un error 400 en vez de un 500
            raise ValidationError({"detail": "El nombre de usuario o el DNI ya están registrados."})


class ListaDeseosPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaDeseosProductos
        fields=[
            'producto'
        ]
        read_only_fields = ['id', 'fecha_at', 'is_active','usuario',]

class ListaDeseosGetSerializer(serializers.ModelSerializer):
    usuario = UsuarioPublicSerializer(read_only=True)
    producto = ProductoListSerializer(read_only=True)

    class Meta:
        model = ListaDeseosProductos
        fields=[
            'id',
            'usuario',
            'producto'
        ]

