from django.test import TestCase
from django.contrib.auth.models import Group
from usuarios.models import UsuarioPersonalizado
from catalogo.models import Producto, Categoria, Marca
from .models import Venta, DetalleVenta


class VentasModelTest(TestCase):
    def setUp(self):
        self.grupo_cliente, _ = Group.objects.get_or_create(name='Cliente')
        self.cliente = UsuarioPersonalizado.objects.create_user(
            username='cliente1',
            password='testpass123',
            email='cliente@test.com'
        )
        self.cliente.groups.add(self.grupo_cliente)
        self.categoria = Categoria.objects.create(
            nombre='Electrodomésticos'
        )
        self.marca = Marca.objects.create(
            nombre='Samsung'
        )
        self.producto = Producto.objects.create(
            nombre='Televisor',
            sku='TV-001',
            precio_lista=500.00,
            stock_total=10,
            marca=self.marca,
            categoria=self.categoria,
        )
        self.venta = Venta.objects.create(
            cliente=self.cliente,
            estado='pendiente',
            nro_factura='V001-0001'
        )
        self.detalle_venta = DetalleVenta.objects.create(
            venta=self.venta,
            producto=self.producto,
            unidades=1,
            precio_unitario=500.00
        )

    def test_crear_venta(self):
        self.assertEqual(self.venta.cliente, self.cliente)
        self.assertEqual(self.venta.estado, 'pendiente')
        self.assertEqual(self.venta.nro_factura, 'V001-0001')

    def test_venta_str_retorna_id_y_cliente(self):
        resultado = str(self.venta)
        self.assertIn('Venta', resultado)
        self.assertIn('cliente1', resultado)

    def test_detalle_venta_str_retorna_venta_y_producto(self):
        resultado = str(self.detalle_venta)
        self.assertIn(str(self.venta.id), resultado)
        self.assertIn('Televisor', resultado)
