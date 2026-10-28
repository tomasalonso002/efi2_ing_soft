import django
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from django.contrib.auth.models import Group
from usuarios.models import UsuarioPersonalizado
from catalogo.models import Categoria, Marca, Producto
from proveedores.models import Proveedor
from compras.models import Compra, DetalleCompra
from ventas.models import Venta, DetalleVenta

print("Limpiando datos existentes...")
from django.db import connection
# Borrar en orden inverso de dependencias para evitar FK constraints
DetalleVenta.objects.all().delete()
DetalleCompra.objects.all().delete()
Venta.objects.all().delete()
Compra.objects.all().delete()
Producto.objects.all().delete()
Proveedor.objects.all().delete()
Marca.objects.all().delete()
Categoria.objects.all().delete()
UsuarioPersonalizado.objects.filter(is_superuser=False).delete()
Group.objects.all().delete()

print("Creando grupos...")
grupo_vendedor, _ = Group.objects.get_or_create(name='Vendedor')
grupo_cliente, _ = Group.objects.get_or_create(name='Cliente')

print("Creando usuarios...")
vendedor, _ = UsuarioPersonalizado.objects.get_or_create(
    username='vendedor1',
    defaults={'email': 'vendedor@test.com', 'telefono': '3581111111', 'dni': '11111111'}
)
if not vendedor.check_password('testpass123'):
    vendedor.set_password('testpass123')
    vendedor.save()
vendedor.groups.add(grupo_vendedor)

cliente, _ = UsuarioPersonalizado.objects.get_or_create(
    username='cliente1',
    defaults={'email': 'cliente@test.com', 'telefono': '3582222222', 'dni': '22222222'}
)
if not cliente.check_password('testpass123'):
    cliente.set_password('testpass123')
    cliente.save()
cliente.groups.add(grupo_cliente)

admin, _ = UsuarioPersonalizado.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@test.com', 'is_superuser': True, 'is_staff': True}
)
if not admin.check_password('admin'):
    admin.set_password('admin')
    admin.save()

print("Creando categorias...")
categorias = [
    Categoria.objects.get_or_create(nombre='Computadoras', descripcion='Laptops y desktops')[0],
    Categoria.objects.get_or_create(nombre='Componentes', descripcion='Placas base, procesadores, tarjetas de video')[0],
    Categoria.objects.get_or_create(nombre='Almacenamiento', descripcion='SSD, discos rígidos, memorias USB')[0],
    Categoria.objects.get_or_create(nombre='Periféricos', descripcion='Teclados, mouse, auriculares')[0],
    Categoria.objects.get_or_create(nombre='Monitores', descripcion='Pantallas y monitores')[0],
    Categoria.objects.get_or_create(nombre='Redes', descripcion='Routers, switches, módems')[0],
    Categoria.objects.get_or_create(nombre='Impresoras', descripcion='Impresoras y escáneres')[0],
]

print("Creando marcas...")
marcas = [
    Marca.objects.get_or_create(nombre='Dell', pais_origen='Estados Unidos', logo='https://example.com/dell.png')[0],
    Marca.objects.get_or_create(nombre='HP', pais_origen='Estados Unidos', logo='https://example.com/hp.png')[0],
    Marca.objects.get_or_create(nombre='Lenovo', pais_origen='China', logo='https://example.com/lenovo.png')[0],
    Marca.objects.get_or_create(nombre='ASUS', pais_origen='Taiwán', logo='https://example.com/asus.png')[0],
    Marca.objects.get_or_create(nombre='MSI', pais_origen='Taiwán', logo='https://example.com/msi.png')[0],
    Marca.objects.get_or_create(nombre='Kingston', pais_origen='Estados Unidos', logo='https://example.com/kingston.png')[0],
    Marca.objects.get_or_create(nombre='Corsair', pais_origen='Estados Unidos', logo='https://example.com/corsair.png')[0],
]

print("Creando productos...")
productos_data = [
    {'nombre': 'Laptop Dell Latitude 5430', 'sku': 'LAP-DELL-5430', 'descripcion_corta': 'Laptop Dell 14 pulgadas', 'descripcion_larga': 'Laptop Dell Latitude 5430 Core i5 16GB RAM 512GB SSD', 'precio_lista': 450000.00, 'precio_oferta': 399999.00, 'stock_total': 15, 'marca_idx': 0, 'categoria_idx': 0, 'destacado': True},
    {'nombre': 'Desktop HP Pavilion', 'sku': 'DES-HP-PAV', 'descripcion_corta': 'Desktop HP Pavilion', 'descripcion_larga': 'Desktop HP Pavilion Core i7 32GB RAM 1TB SSD', 'precio_lista': 280000.00, 'precio_oferta': 249999.00, 'stock_total': 8, 'marca_idx': 1, 'categoria_idx': 0, 'destacado': False},
    {'nombre': 'Memoria RAM Kingston 16GB DDR4', 'sku': 'RAM-KIN-16GB', 'descripcion_corta': 'RAM 16GB DDR4 3200MHz', 'descripcion_larga': 'Memoria RAM Kingston Fury 16GB DDR4 3200MHz', 'precio_lista': 85000.00, 'precio_oferta': 69999.00, 'stock_total': 30, 'marca_idx': 5, 'categoria_idx': 2, 'destacado': True},
    {'nombre': 'SSD Corsair 1TB NVMe', 'sku': 'SSD-COR-1TB', 'descripcion_corta': 'SSD 1TB NVMe M.2', 'descripcion_larga': 'SSD Corsair MP600 1TB NVMe M.2 Gen4', 'precio_lista': 25000.00, 'precio_oferta': 19999.00, 'stock_total': 50, 'marca_idx': 6, 'categoria_idx': 2, 'destacado': False},
    {'nombre': 'Teclado Mecánico Corsair', 'sku': 'TEC-COR-MEC', 'descripcion_corta': 'Teclado mecánico RGB', 'descripcion_larga': 'Teclado mecánico Corsair K70 RGB con switches Cherry MX', 'precio_lista': 15000.00, 'precio_oferta': None, 'stock_total': 20, 'marca_idx': 6, 'categoria_idx': 3, 'destacado': False},
    {'nombre': 'Mouse Gaming ASUS', 'sku': 'MOU-ASU-GAM', 'descripcion_corta': 'Mouse gaming RGB', 'descripcion_larga': 'Mouse gaming ASUS ROG Gladius con sensor óptico', 'precio_lista': 60000.00, 'precio_oferta': 49999.00, 'stock_total': 12, 'marca_idx': 3, 'categoria_idx': 3, 'destacado': False},
    {'nombre': 'Monitor Lenovo 27"', 'sku': 'MON-LEN-27', 'descripcion_corta': 'Monitor 27 pulgadas IPS', 'descripcion_larga': 'Monitor Lenovo 27 pulgadas IPS Full HD 75Hz', 'precio_lista': 45000.00, 'precio_oferta': None, 'stock_total': 25, 'marca_idx': 2, 'categoria_idx': 4, 'destacado': False},
    {'nombre': 'Tarjeta de Video MSI RTX 4060', 'sku': 'GPU-MSI-4060', 'descripcion_corta': 'GPU MSI RTX 4060 8GB', 'descripcion_larga': 'Tarjeta de video MSI GeForce RTX 4060 Ventus 2X 8GB GDDR6', 'precio_lista': 320000.00, 'precio_oferta': None, 'stock_total': 5, 'marca_idx': 4, 'categoria_idx': 1, 'destacado': False},
    {'nombre': 'Impresora HP DeskJet', 'sku': 'IMP-HP-DESK', 'descripcion_corta': 'Impresora multifunción', 'descripcion_larga': 'Impresora HP DeskJet 2720 multifunción WiFi', 'precio_lista': 12000.00, 'precio_oferta': None, 'stock_total': 40, 'marca_idx': 1, 'categoria_idx': 6, 'destacado': False},
    {'nombre': 'Router ASUS WiFi 6', 'sku': 'ROU-ASU-W6', 'descripcion_corta': 'Router WiFi 6', 'descripcion_larga': 'Router ASUS RT-AX55 WiFi 6 dual banda', 'precio_lista': 520000.00, 'precio_oferta': 479999.00, 'stock_total': 7, 'marca_idx': 3, 'categoria_idx': 5, 'destacado': True},
]

productos = []
for pd in productos_data:
    p, _ = Producto.objects.get_or_create(
        sku=pd['sku'],
        defaults={
            'nombre': pd['nombre'],
            'descripcion_corta': pd['descripcion_corta'],
            'descripcion_larga': pd['descripcion_larga'],
            'precio_lista': pd['precio_lista'],
            'precio_oferta': pd['precio_oferta'],
            'stock_total': pd['stock_total'],
            'marca': marcas[pd['marca_idx']],
            'categoria': categorias[pd['categoria_idx']],
            'destacado': pd['destacado'],
        }
    )
    productos.append(p)

print("Creando proveedores...")
proveedores = [
    Proveedor.objects.get_or_create(
        cuit='20-12345678-9',
        defaults={'nombre': 'Tech Distribuidor SA', 'email': 'contacto@techdist.com.ar', 'telefono': '3583333333', 'direccion': 'Av. San Martín 1234, Río Cuarto'}
    )[0],
    Proveedor.objects.get_or_create(
        cuit='20-98765432-1',
        defaults={'nombre': 'Hogar y Más', 'email': 'ventas@hogarymas.com.ar', 'telefono': '3584444444', 'direccion': 'Calle Colón 567, Río Cuarto'}
    )[0],
    Proveedor.objects.get_or_create(
        cuit='20-55555555-5',
        defaults={'nombre': 'Deportes Centro', 'email': 'info@deportescentro.com.ar', 'telefono': '3585555555', 'direccion': 'Bulevar Belgrano 890, Río Cuarto'}
    )[0],
]

print("Creando compras...")
compra1, _ = Compra.objects.get_or_create(
    nro_factura='F001-0001',
    defaults={'proveedor': proveedores[0], 'estado': 'recibida', 'total': 0}
)
compra2, _ = Compra.objects.get_or_create(
    nro_factura='F002-0005',
    defaults={'proveedor': proveedores[1], 'estado': 'pendiente', 'total': 0}
)
compra3, _ = Compra.objects.get_or_create(
    nro_factura='F003-0010',
    defaults={'proveedor': proveedores[2], 'estado': 'cancelada', 'total': 0}
)

print("Creando detalles de compra...")
DetalleCompra.objects.get_or_create(
    compra=compra1, producto=productos[0], defaults={'unidades': 5, 'precio': 399999.00}
)
DetalleCompra.objects.get_or_create(
    compra=compra1, producto=productos[2], defaults={'unidades': 10, 'precio': 69999.00}
)
DetalleCompra.objects.get_or_create(
    compra=compra2, producto=productos[4], defaults={'unidades': 20, 'precio': 15000.00}
)
DetalleCompra.objects.get_or_create(
    compra=compra3, producto=productos[7], defaults={'unidades': 3, 'precio': 320000.00}
)

print("Creando ventas...")
venta1, _ = Venta.objects.get_or_create(
    nro_factura='V001-0001',
    defaults={'cliente': cliente, 'estado': 'completada'}
)
venta2, _ = Venta.objects.get_or_create(
    nro_factura='V001-0002',
    defaults={'cliente': vendedor, 'estado': 'pendiente'}
)
venta3, _ = Venta.objects.get_or_create(
    nro_factura='V001-0003',
    defaults={'cliente': cliente, 'estado': 'cancelada'}
)

print("Creando detalles de venta...")
DetalleVenta.objects.get_or_create(
    venta=venta1, producto=productos[1], defaults={'unidades': 2, 'precio_unitario': 249999.00}
)
DetalleVenta.objects.get_or_create(
    venta=venta1, producto=productos[3], defaults={'unidades': 1, 'precio_unitario': 19999.00}
)
DetalleVenta.objects.get_or_create(
    venta=venta2, producto=productos[5], defaults={'unidades': 1, 'precio_unitario': 49999.00}
)

print("\n=== BASE DE DATOS CARGADA ===")
print(f"Usuarios: {UsuarioPersonalizado.objects.count()}")
print(f"Categorías: {Categoria.objects.count()}")
print(f"Marcas: {Marca.objects.count()}")
print(f"Productos: {Producto.objects.count()}")
print(f"Proveedores: {Proveedor.objects.count()}")
print(f"Compras: {Compra.objects.count()}")
print(f"Detalles de Compra: {DetalleCompra.objects.count()}")
print(f"Ventas: {Venta.objects.count()}")
print(f"Detalles de Venta: {DetalleVenta.objects.count()}")
print("\nCredenciales:")
print("  admin / admin (superuser)")
print("  vendedor1 / testpass123 (grupo Vendedor)")
print("  cliente1 / testpass123 (grupo Cliente)")
