from django.test import TestCase
from .models import Proveedor


class ProveedorModelTest(TestCase):
    def setUp(self):
        self.proveedor = Proveedor.objects.create(
            nombre='Tech Distribuidor',
            cuit='20-12345678-9',
            email='contacto@tech.com',
            telefono='3581234567',
            direccion='Calle Falsa 123'
        )

    def test_crear_proveedor(self):
        self.assertEqual(self.proveedor.nombre, 'Tech Distribuidor')
        self.assertEqual(self.proveedor.cuit, '20-12345678-9')
        self.assertEqual(self.proveedor.email, 'contacto@tech.com')

    def test_proveedor_str_retorna_nombre(self):
        self.assertEqual(str(self.proveedor), 'Tech Distribuidor')

    def test_proveedor_tiene_is_active_true_por_defecto(self):
        self.assertTrue(self.proveedor.is_active)
