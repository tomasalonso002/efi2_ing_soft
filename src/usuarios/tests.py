from django.test import TestCase
from django.contrib.auth.models import Group
from usuarios.models import UsuarioPersonalizado


class UsuarioModelTest(TestCase):
    def setUp(self):
        self.grupo_vendedor, _ = Group.objects.get_or_create(name='Vendedor')
        self.usuario = UsuarioPersonalizado.objects.create_user(
            username='cliente1',
            password='testpass123',
            email='cliente@test.com',
            telefono='123456789',
            dni='12345678'
        )

    def test_crear_usuario_personalizado(self):
        self.assertEqual(self.usuario.username, 'cliente1')
        self.assertEqual(self.usuario.email, 'cliente@test.com')
        self.assertEqual(self.usuario.telefono, '123456789')
        self.assertEqual(self.usuario.dni, '12345678')

    def test_usuario_str_contiene_username_y_dni(self):
        resultado = str(self.usuario)
        self.assertIn('cliente1', resultado)
        self.assertIn('12345678', resultado)

    def test_usuario_tiene_is_active_true_por_defecto(self):
        self.assertTrue(self.usuario.is_active)
