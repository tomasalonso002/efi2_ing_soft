from django.contrib import admin
from .models import Categoria, Marca, Producto, DetalleCompra, Compra, DetalleVenta, Venta, Proveedor, ProductoImagen

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Producto)
admin.site.register(DetalleCompra)
admin.site.register(Compra)
admin.site.register(DetalleVenta)
admin.site.register(Venta)
admin.site.register(Proveedor)
admin.site.register(ProductoImagen)