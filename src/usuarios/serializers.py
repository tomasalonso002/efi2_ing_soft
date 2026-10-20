from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import UsuarioPersonalizado

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
            'id',
            'username',
            'last_name',
            'first_name',
            'password',
            'telefono',
            'email',
            'dni',
        ]
        read_only_fields=['id']
        #Indica que el campo 'password' es de solo escritura
        extra_kwargs = {
            'password': {'write_only': True}
            }
        

        
