from django.test import TestCase
from .models import Categoria, Marca, Producto


class CatalogoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre='Electrodomésticos',
            descripcion='Productos eléctricos'
        )
        self.marca = Marca.objects.create(
            nombre='Samsung',
            pais_origen='Corea del Sur'
        )
        self.producto = Producto.objects.create(
            nombre='Televisor',
            sku='TV-001',
            precio_lista=500.00,
            stock_total=10,
            marca=self.marca,
            categoria=self.categoria,
        )

    def test_crear_categoria(self):
        self.assertEqual(self.categoria.nombre, 'Electrodomésticos')
        self.assertTrue(self.categoria.is_active)

    def test_producto_str_retorna_nombre(self):
        self.assertEqual(str(self.producto), 'Televisor')

    def test_producto_esta_relacionado_con_marca_y_categoria(self):
        self.assertEqual(self.producto.marca, self.marca)
        self.assertEqual(self.producto.categoria, self.categoria)
        self.assertIn(self.producto, self.marca.productos.all())
        self.assertIn(self.producto, self.categoria.productos.all())
