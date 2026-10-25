from django.db import models


class Proveedor(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    cuit = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=150,
        blank=True
    )
    telefono = models.CharField(max_length=50, blank=True)
    direccion = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
