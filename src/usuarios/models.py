from django.db import models
from django.contrib.auth.models import AbstractUser
from catalogo.models import Producto

# Create your models here.
class UsuarioPersonalizado(AbstractUser):
    telefono = models.CharField(max_length=20, null= True, blank=True)
    dni = models.CharField(null=True, blank=True)
    def __str__(self):
        return f'{self.username} - {self.dni}'


class ListaDeseosProductos(models.Model):
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='usuario_lista_deseos', null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='producto_lista_deseos', null=True, blank=True)
    fecha_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
            return f'{self.usuario.username} - {self.producto.nombre}'

