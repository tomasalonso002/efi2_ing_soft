import random
from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.utils import timezone
from faker import Faker

from catalogo.models import Categoria, Marca, Producto
from proveedores.models import Proveedor
from ventas.models import Venta, DetalleVenta
from compras.models import Compra, DetalleCompra

Usuario = get_user_model()

fake = Faker('es_ES')

MARCAS_TECNOLOGIA = [
    'Asus', 'HP', 'Lenovo', 'Logitech', 'Samsung', 'LG', 'MSI',
    'Gigabyte', 'Corsair', 'Razer', 'Dell', 'Acer', 'Xiaomi'
]

CATEGORIAS_TECNOLOGIA = [
    ('Notebooks', 'Computadoras portátiles'),
    ('Monitores', 'Pantallas y monitores'),
    ('Periféricos', 'Teclados, ratones, auriculares'),
    ('Componentes', 'Partes internas de PC'),
    ('Almacenamiento', 'Discos duros, SSD, USB'),
    ('Redes', 'Routers, switches, cables'),
    ('Impresoras', 'Impresoras y consumibles'),
    ('Audio', 'Parlantes, micrófonos, auriculares'),
    ('Gaming', 'Productos para gaming'),
    ('Accesorios', 'Fundas, soportes, cables'),
]

PRODUCTOS_POR_CATEGORIA = {
    'Notebooks': ['Notebook {marca} {modelo}', 'Laptop {marca} {modelo}'],
    'Monitores': ['Monitor {marca} {pulgadas}"', 'Pantalla {marca} {pulgadas}"'],
    'Periféricos': ['Teclado {marca} {modelo}', 'Mouse {marca} {modelo}', 'Auriculares {marca} {modelo}'],
    'Componentes': ['Placa Madre {marca} {modelo}', 'Fuente {marca} {modelo}', 'Gabinete {marca} {modelo}'],
    'Almacenamiento': ['SSD {marca} {capacidad}', 'Disco Duro {marca} {capacidad}', 'Memoria USB {marca} {capacidad}'],
    'Redes': ['Router {marca} {modelo}', 'Switch {marca} {modelo}'],
    'Impresoras': ['Impresora {marca} {modelo}', 'Tóner {marca} {modelo}'],
    'Audio': ['Parlantes {marca} {modelo}', 'Micrófono {marca} {modelo}'],
    'Gaming': ['Silla Gaming {marca} {modelo}', 'Alfombrilla {marca} {modelo}'],
    'Accesorios': ['Funda {marca} {modelo}', 'Soporte {marca} {modelo}', 'Cable {marca} {modelo}'],
}

MODELOS = ['Pro', 'Elite', 'Ultra', 'Max', 'Plus', 'Air', 'Gaming', 'Business', 'Home', 'Student']
PULGADAS = ['21.5', '23.8', '24', '27', '32', '34', '49']
CAPACIDADES = ['256GB', '512GB', '1TB', '2TB', '4TB', '8TB', '128GB', '64GB', '32GB']


class Command(BaseCommand):
    help = 'Genera datos de prueba completos y realistas para el proyecto'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina los datos de prueba existentes antes de crear nuevos',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Eliminando datos de prueba existentes...')
            DetalleVenta.objects.all().delete()
            Venta.objects.all().delete()
            DetalleCompra.objects.all().delete()
            Compra.objects.all().delete()
            Producto.objects.all().delete()
            Categoria.objects.all().delete()
            Marca.objects.all().delete()
            Proveedor.objects.all().delete()
            Usuario.objects.filter(is_superuser=False).delete()
            Group.objects.filter(name__in=['Cliente', 'Vendedor']).delete()

        self.stdout.write('Creando grupos de usuarios...')
        self._crear_grupos()

        self.stdout.write('Creando usuarios (clientes, vendedores, admin)...')
        clientes, vendedores, admin = self._crear_usuarios()

        self.stdout.write('Creando marcas y categorías...')
        marcas = self._crear_marcas()
        categorias = self._crear_categorias()

        self.stdout.write('Creando productos...')
        productos = self._crear_productos(marcas, categorias)

        self.stdout.write('Creando proveedores...')
        proveedores = self._crear_proveedores()

        self.stdout.write('Generando 20 Ventas...')
        self._crear_ventas(clientes, vendedores, productos)

        self.stdout.write('Generando 20 Compras...')
        self._crear_compras(proveedores, productos)

        self.stdout.write(
            self.style.SUCCESS(
                '¡Base de datos poblada exitosamente con datos realistas!'
            )
        )

    def _crear_grupos(self):
        Group.objects.get_or_create(name='Cliente')
        Group.objects.get_or_create(name='Vendedor')
        Group.objects.get_or_create(name='Administrador')

    def _crear_usuarios(self):
        grupo_cliente = Group.objects.get(name='Cliente')
        grupo_vendedor = Group.objects.get(name='Vendedor')
        grupo_admin = Group.objects.get(name='Administrador')

        clientes = []
        for i in range(20):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f'{first_name.lower()}{last_name.lower()}{fake.random_number(digits=2)}'.replace(' ', '')
            email = f'{username}@email.com'
            
            cliente, _ = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'dni': f'{random.randint(10000000, 99999999)}',
                    'telefono': fake.phone_number(),
                    'is_active': True,
                }
            )
            cliente.groups.add(grupo_cliente)
            clientes.append(cliente)

        vendedores = []
        for i in range(2):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f'vendedor_{first_name.lower()}{last_name.lower()}'
            
            vendedor, _ = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@empresa.com',
                    'first_name': first_name,
                    'last_name': last_name,
                    'dni': f'{random.randint(10000000, 99999999)}',
                    'telefono': fake.phone_number(),
                    'is_active': True,
                    'is_staff': True,
                }
            )
            vendedor.groups.add(grupo_vendedor)
            vendedores.append(vendedor)

        admin, _ = Usuario.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@empresa.com',
                'first_name': 'Admin',
                'last_name': 'Sistema',
                'dni': '00000000',
                'telefono': '0000000000',
                'is_active': True,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin.groups.add(grupo_admin)
        admin.set_password('admin123')
        admin.save()

        return clientes, vendedores, admin

    def _crear_marcas(self):
        marcas = []
        for nombre in MARCAS_TECNOLOGIA:
            marca, _ = Marca.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': f'Marca {nombre} - Tecnología de calidad',
                    'pais_origen': fake.country(),
                    'is_active': True,
                }
            )
            marcas.append(marca)
        return marcas

    def _crear_categorias(self):
        categorias = []
        for nombre, descripcion in CATEGORIAS_TECNOLOGIA:
            categoria, _ = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': descripcion,
                    'is_active': True,
                }
            )
            categorias.append(categoria)
        return categorias

    def _crear_productos(self, marcas, categorias):
        productos = []
        cat_dict = {c.nombre: c for c in categorias}
        marca_dict = {m.nombre: m for m in marcas}

        for i in range(25):
            categoria = random.choice(categorias)
            marca = random.choice(marcas)
            
            templates = PRODUCTOS_POR_CATEGORIA.get(categoria.nombre, ['{marca} {modelo}'])
            template = random.choice(templates)
            
            modelo = random.choice(MODELOS)
            pulgadas = random.choice(PULGADAS)
            capacidad = random.choice(CAPACIDADES)
            
            nombre = template.format(
                marca=marca.nombre,
                modelo=modelo,
                pulgadas=pulgadas,
                capacidad=capacidad
            )
            
            sku = f'{marca.nombre[:3].upper()}-{categoria.nombre[:3].upper()}-{i+1:04d}'
            
            precio_lista = Decimal(random.uniform(20000, 500000)).quantize(Decimal('0.01'))
            tiene_oferta = random.choice([True, False])
            precio_oferta = Decimal(random.uniform(15000, float(precio_lista) * 0.9)).quantize(Decimal('0.01')) if tiene_oferta else None
            
            producto, _ = Producto.objects.get_or_create(
                sku=sku,
                defaults={
                    'nombre': nombre,
                    'descripcion_corta': f'{nombre} - {fake.sentence(nb_words=10)}',
                    'descripcion_larga': fake.paragraph(nb_sentences=3),
                    'precio_lista': precio_lista,
                    'precio_oferta': precio_oferta,
                    'stock_total': random.randint(5, 200),
                    'marca': marca,
                    'categoria': categoria,
                    'is_active': True,
                    'destacado': random.choice([True, False]),
                }
            )
            productos.append(producto)
        return productos

    def _crear_proveedores(self):
        proveedores = []
        sufijos = ['S.A.', 'S.R.L.', 'S.A.S.', 'S.C.A.', 'S.E.']
        
        for i in range(20):
            nombre_base = fake.company()
            nombre = f'{nombre_base} {random.choice(sufijos)}'
            
            cuit = f'{random.randint(20, 30)}-{random.randint(10000000, 99999999)}-{random.randint(0, 9)}'
            
            proveedor, _ = Proveedor.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'cuit': cuit,
                    'email': f'compras@{nombre_base.lower().replace(" ", "").replace(".", "")}.com.ar',
                    'telefono': fake.phone_number(),
                    'direccion': fake.street_address() + ', ' + fake.city(),
                    'is_active': True,
                }
            )
            proveedores.append(proveedor)
        return proveedores

    def _crear_ventas(self, clientes, vendedores, productos):
        estados = ['pendiente', 'completada', 'cancelada']
        pesos_estados = [0.2, 0.7, 0.1]
        
        ahora = timezone.now()
        tres_meses_atras = ahora - timedelta(days=90)
        
        for i in range(20):
            cliente = random.choice(clientes)
            vendedor = random.choice(vendedores)
            estado = random.choices(estados, weights=pesos_estados)[0]
            
            fecha_venta = fake.date_time_between(start_date=tres_meses_atras, end_date=ahora, tzinfo=timezone.get_current_timezone())
            
            venta = Venta.objects.create(
                cliente=cliente,
                estado=estado,
                nro_factura=f'FAC-{fecha_venta.strftime("%Y%m%d")}-{i+1:04d}',
                is_active=True,
                created_at=fecha_venta,
            )
            
            num_detalles = random.randint(1, 4)
            productos_venta = random.sample(productos, min(num_detalles, len(productos)))
            total_venta = Decimal('0.00')
            
            for producto in productos_venta:
                unidades = random.randint(1, 5)
                precio_unitario = producto.precio_oferta if producto.precio_oferta else producto.precio_lista
                subtotal = precio_unitario * unidades
                total_venta += subtotal
                
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    unidades=unidades,
                    precio_unitario=precio_unitario,
                    is_active=True,
                    created_at=fecha_venta,
                )
            
            venta.nro_factura = f'FAC-{fecha_venta.strftime("%Y%m%d")}-{i+1:04d}'
            venta.save(update_fields=['nro_factura'])

    def _crear_compras(self, proveedores, productos):
        estados = ['pendiente', 'recibida', 'cancelada']
        pesos_estados = [0.2, 0.7, 0.1]
        
        ahora = timezone.now()
        tres_meses_atras = ahora - timedelta(days=90)
        
        for i in range(20):
            proveedor = random.choice(proveedores)
            estado = random.choices(estados, weights=pesos_estados)[0]
            
            fecha_compra = fake.date_time_between(start_date=tres_meses_atras, end_date=ahora, tzinfo=timezone.get_current_timezone())
            
            compra = Compra.objects.create(
                proveedor=proveedor,
                estado=estado,
                nro_factura=f'COM-{fecha_compra.strftime("%Y%m%d")}-{i+1:04d}',
                total=Decimal('0.00'),
                is_active=True,
                created_at=fecha_compra,
            )
            
            num_detalles = random.randint(1, 4)
            productos_compra = random.sample(productos, min(num_detalles, len(productos)))
            total_compra = Decimal('0.00')
            
            for producto in productos_compra:
                unidades = random.randint(5, 50)
                precio = Decimal(random.uniform(10000, 300000)).quantize(Decimal('0.01'))
                subtotal = precio * unidades
                total_compra += subtotal
                
                DetalleCompra.objects.create(
                    compra=compra,
                    producto=producto,
                    unidades=unidades,
                    precio=precio,
                    is_active=True,
                    created_at=fecha_compra,
                )
            
            compra.total = total_compra
            compra.nro_factura = f'COM-{fecha_compra.strftime("%Y%m%d")}-{i+1:04d}'
            compra.save(update_fields=['total', 'nro_factura'])