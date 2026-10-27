from django.db import models


class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    logo = models.CharField(max_length=500, blank=True)
    descripcion = models.TextField(blank=True)
    pais_origen = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion_corta = models.CharField(max_length=500, blank=True)
    descripcion_larga = models.TextField(blank=True)
    sku = models.CharField(max_length=100, unique=True)
    precio_lista = models.DecimalField(max_digits=12, decimal_places=2)
    precio_oferta = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    imagen_url = models.CharField(max_length=500, blank=True)
    stock_total = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        related_name='productos'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
