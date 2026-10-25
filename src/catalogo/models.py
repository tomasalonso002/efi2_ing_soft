from django.db import models
from django.conf import settings


class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False)
    descripcion = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    def __str__(self):
        return self.nombre

class Marca(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False)
    logo = models.CharField(max_length=500, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    pais_origen = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=200, null=False)
    descripcion_corta = models.CharField(max_length=500, blank=True, null=True)
    descripcion_larga = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True, null=False)
    precio_lista = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    precio_oferta = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock_total = models.IntegerField(default=0, null=False)
    is_active = models.BooleanField(default=True, null=False)
    destacado = models.BooleanField(default=False, null=False)
    marca = models.ForeignKey(Marca,on_delete=models.PROTECT,null=False,related_name='productos')
    categoria = models.ForeignKey(Categoria,on_delete=models.PROTECT,null=False,related_name='productos')
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    def __str__(self):
        return self.nombre
    
class ProductoImagen(models.Model):
    id = models.BigAutoField(primary_key=True)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE,null=False,related_name='imagenes')
    imagen_url = models.CharField(max_length=500, null=False)
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    es_principal = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=True, null=False)
    def __str__(self):
        return f'Imagen de {self.producto.nombre}'
    
class Proveedor(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False)
    cuit = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    def __str__(self):
        return self.nombre

#DETALLE COMPRA
class Compra(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('recibida', 'Recibida'),
        ('cancelada', 'Cancelada'),
    ]
    id = models.BigAutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.PROTECT,null=False,related_name='compras')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', null=False)
    nro_factura = models.CharField(max_length=50, blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=True, null=False)
    def __str__(self):
        return f'Compra {self.id} - {self.proveedor.nombre}'

class DetalleCompra(models.Model):
    id = models.BigAutoField(primary_key=True)
    compra = models.ForeignKey(Compra,on_delete=models.PROTECT,null=False,related_name='detalle_compra')
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE,null=False,related_name='detalle_compra_producto')
    unidades = models.PositiveIntegerField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=True, null=False)
    def __str__(self):
        return f'Compra {self.id} - Nro_factura:{self.compra.nro_factura}'

#DETALLE VENTA
class Venta(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    id = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey('usuarios.UsuarioPersonalizado', on_delete=models.PROTECT, null=False, related_name='ventas',)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', null=False)
    nro_factura = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=True, null=False)
    def __str__(self):
        return f'Venta {self.id} - Cliente: {self.cliente.username}'

class DetalleVenta(models.Model):
    id = models.BigAutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null=False, related_name='venta_detalle_venta')
    producto = models.ForeignKey(Producto,on_delete=models.PROTECT,null=False,related_name='producto_detalle_venta',)
    unidades = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=True, null=False)
    def __str__(self):
        return f'Detalle Venta {self.venta.id} - {self.producto.nombre}'


