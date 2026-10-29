import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from catalogo.models import Categoria, Marca, Producto
from proveedores.models import Proveedor
from ventas.models import Venta, DetalleVenta
from compras.models import Compra, DetalleCompra

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Genera datos de prueba para Ventas y Compras'

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
            DetalleVenta.objects.filter(venta__nro_factura__startswith='FAC-SEED-').delete()
            Venta.objects.filter(nro_factura__startswith='FAC-SEED-').delete()
            DetalleCompra.objects.filter(compra__nro_factura__startswith='COM-SEED-').delete()
            Compra.objects.filter(nro_factura__startswith='COM-SEED-').delete()
            Producto.objects.filter(sku__startswith='SEED-').delete()
            Categoria.objects.filter(nombre__startswith='SEED ').delete()
            Marca.objects.filter(nombre__startswith='SEED ').delete()
            Proveedor.objects.filter(nombre__startswith='SEED ').delete()
            Usuario.objects.filter(username__startswith='cliente_seed_').delete()
            Usuario.objects.filter(username__startswith='vendedor_seed_').delete()

        if Venta.objects.filter(nro_factura__startswith='FAC-SEED-').exists() or \
           Compra.objects.filter(nro_factura__startswith='COM-SEED-').exists():
            self.stdout.write(self.style.WARNING('Los datos de prueba ya existen. Usa --clear para regenerarlos.'))
            return

        self.stdout.write('Creando datos base...')

        categorias = self._crear_categorias()
        marcas = self._crear_marcas()
        productos = self._crear_productos(categorias, marcas)
        clientes = self._crear_clientes()
        vendedores = self._crear_vendedores()
        proveedores = self._crear_proveedores()

        self.stdout.write('Generando 10 Ventas...')
        ventas_creadas = self._crear_ventas(clientes, vendedores, productos)

        self.stdout.write('Generando 10 Compras...')
        compras_creadas = self._crear_compras(proveedores, productos)

        self.stdout.write(
            self.style.SUCCESS(
                f'¡{ventas_creadas} Ventas y {compras_creadas} Compras generadas con éxito!'
            )
        )

    def _crear_categorias(self):
        nombres = ['SEED Electrónica', 'SEED Ropa', 'SEED Hogar', 'SEED Deportes', 'SEED Libros']
        categorias = []
        for nombre in nombres:
            cat, _ = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': f'Categoría de prueba: {nombre}'}
            )
            categorias.append(cat)
        return categorias

    def _crear_marcas(self):
        nombres = ['SEED TechBrand', 'SEED FashionCo', 'SEED HomeStyle', 'SEED SportLine', 'SEED BookWorld']
        marcas = []
        for nombre in nombres:
            marca, _ = Marca.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': f'Marca de prueba: {nombre}', 'pais_origen': 'Argentina'}
            )
            marcas.append(marca)
        return marcas

    def _crear_productos(self, categorias, marcas):
        productos = []
        for i in range(15):
            sku = f'SEED-PROD-{i+1:03d}'
            producto, created = Producto.objects.get_or_create(
                sku=sku,
                defaults={
                    'nombre': f'Producto Seed {i+1}',
                    'descripcion_corta': f'Descripción corta del producto {i+1}',
                    'descripcion_larga': f'Descripción larga y detallada del producto de prueba número {i+1}.',
                    'precio_lista': Decimal(random.uniform(500, 50000)).quantize(Decimal('0.01')),
                    'precio_oferta': Decimal(random.uniform(400, 45000)).quantize(Decimal('0.01')),
                    'stock_total': random.randint(10, 500),
                    'marca': random.choice(marcas),
                    'categoria': random.choice(categorias),
                    'is_active': True,
                    'destacado': random.choice([True, False]),
                }
            )
            productos.append(producto)
        return productos

    def _crear_clientes(self):
        clientes = []
        for i in range(5):
            username = f'cliente_seed_{i+1}'
            cliente, _ = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@test.com',
                    'first_name': f'Cliente',
                    'last_name': f'Prueba {i+1}',
                    'dni': f'{random.randint(10000000, 99999999)}',
                }
            )
            clientes.append(cliente)
        return clientes

    def _crear_vendedores(self):
        vendedores = []
        for i in range(3):
            username = f'vendedor_seed_{i+1}'
            vendedor, _ = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@test.com',
                    'first_name': f'Vendedor',
                    'last_name': f'Prueba {i+1}',
                    'dni': f'{random.randint(10000000, 99999999)}',
                }
            )
            vendedores.append(vendedor)
        return vendedores

    def _crear_proveedores(self):
        proveedores = []
        for i in range(5):
            nombre = f'SEED Proveedor {i+1}'
            proveedor, _ = Proveedor.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'cuit': f'{random.randint(20, 30)}-{random.randint(10000000, 99999999)}-{random.randint(0, 9)}',
                    'email': f'proveedor{i+1}@seedtest.com',
                    'telefono': f'+54 11 {random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                    'direccion': f'Calle Falsa {random.randint(100, 9999)}, CABA',
                    'is_active': True,
                }
            )
            proveedores.append(proveedor)
        return proveedores

    def _crear_ventas(self, clientes, vendedores, productos):
        estados = ['pendiente', 'completada', 'cancelada']
        ventas_creadas = 0

        for i in range(10):
            cliente = random.choice(clientes)
            vendedor = random.choice(vendedores)
            estado = random.choice(estados)

            venta = Venta.objects.create(
                cliente=cliente,
                estado=estado,
                nro_factura=f'FAC-SEED-{i+1:04d}',
                is_active=True,
            )

            num_detalles = random.randint(1, 5)
            productos_venta = random.sample(productos, min(num_detalles, len(productos)))
            total_venta = Decimal('0.00')

            for producto in productos_venta:
                unidades = random.randint(1, 10)
                precio_unitario = producto.precio_oferta if producto.precio_oferta else producto.precio_lista
                subtotal = precio_unitario * unidades
                total_venta += subtotal

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    unidades=unidades,
                    precio_unitario=precio_unitario,
                    is_active=True,
                )

            ventas_creadas += 1

        return ventas_creadas

    def _crear_compras(self, proveedores, productos):
        estados = ['pendiente', 'recibida', 'cancelada']
        compras_creadas = 0

        for i in range(10):
            proveedor = random.choice(proveedores)
            estado = random.choice(estados)

            compra = Compra.objects.create(
                proveedor=proveedor,
                estado=estado,
                nro_factura=f'COM-SEED-{i+1:04d}',
                total=Decimal('0.00'),
                is_active=True,
            )

            num_detalles = random.randint(1, 5)
            productos_compra = random.sample(productos, min(num_detalles, len(productos)))
            total_compra = Decimal('0.00')

            for producto in productos_compra:
                unidades = random.randint(5, 50)
                precio = Decimal(random.uniform(200, 30000)).quantize(Decimal('0.01'))
                subtotal = precio * unidades
                total_compra += subtotal

                DetalleCompra.objects.create(
                    compra=compra,
                    producto=producto,
                    unidades=unidades,
                    precio=precio,
                    is_active=True,
                )

            compra.total = total_compra
            compra.save(update_fields=['total'])
            compras_creadas += 1

        return compras_creadas