from django.test import TestCase
from proveedores.models import Proveedor
from catalogo.models import Producto, Categoria, Marca
from .models import Compra, DetalleCompra


class ComprasModelTest(TestCase):
    def setUp(self):
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
        self.proveedor = Proveedor.objects.create(
            nombre='Tech Distribuidor',
            cuit='20-12345678-9'
        )
        self.compra = Compra.objects.create(
            proveedor=self.proveedor,
            estado='pendiente',
            nro_factura='F001-0001',
            total=500.00
        )
        self.detalle_compra = DetalleCompra.objects.create(
            compra=self.compra,
            producto=self.producto,
            unidades=2,
            precio=250.00
        )

    def test_crear_compra(self):
        self.assertEqual(self.compra.proveedor, self.proveedor)
        self.assertEqual(self.compra.estado, 'pendiente')
        self.assertEqual(self.compra.nro_factura, 'F001-0001')

    def test_compra_str_retorna_id_y_proveedor(self):
        resultado = str(self.compra)
        self.assertIn('Compra', resultado)
        self.assertIn('Tech Distribuidor', resultado)

    def test_detalle_compra_str_retorna_compra_y_producto(self):
        resultado = str(self.detalle_compra)
        self.assertIn(str(self.compra.id), resultado)
        self.assertIn('Televisor', resultado)
