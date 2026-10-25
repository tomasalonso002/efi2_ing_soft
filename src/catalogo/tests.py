from django.test import TestCase
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from .models import (
    Categoria, Marca, Producto, ProductoImagen, Proveedor,
    Compra, DetalleCompra, Venta, DetalleVenta
)
from usuarios.models import UsuarioPersonalizado


class CatalogoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre='Electrodomésticos', descripcion='Productos eléctricos'
        )
        self.marca = Marca.objects.create(
            nombre='Samsung', pais_origen='Corea del Sur'
        )
        self.producto = Producto.objects.create(
            nombre='Televisor',
            sku='TV-001',
            precio_lista=500.00,
            precio_oferta=450.00,
            stock_total=10,
            marca=self.marca,
            categoria=self.categoria,
        )
        self.producto_inactivo = Producto.objects.create(
            nombre='Televisor Viejo',
            sku='TV-002',
            precio_lista=300.00,
            stock_total=0,
            marca=self.marca,
            categoria=self.categoria,
            is_active=False,
        )
        self.proveedor = Proveedor.objects.create(
            nombre='Tech Distribuidor', cuit='20-12345678-9'
        )
        self.usuario = UsuarioPersonalizado.objects.create_user(
            username='cliente1', password='testpass123', email='cliente@test.com'
        )

    def test_producto_soft_delete_renombra_sku(self):
        sku_original = self.producto.sku
        self.producto.is_active = False
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        self.producto.sku = f'delete-{sku_original}-{timestamp}'
        self.producto.save()
        self.assertFalse(self.producto.is_active)
        self.assertTrue(self.producto.sku.startswith('delete-'))

    def test_proveedor_soft_delete_renombra_campos_unicos(self):
        nombre_original = self.proveedor.nombre
        cuit_original = self.proveedor.cuit
        self.proveedor.is_active = False
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        self.proveedor.nombre = f'delete-{nombre_original}-{timestamp}'
        self.proveedor.cuit = f'delete-{cuit_original}-{timestamp}'
        self.proveedor.save()
        self.assertFalse(self.proveedor.is_active)
        self.assertTrue(self.proveedor.nombre.startswith('delete-'))
        self.assertTrue(self.proveedor.cuit.startswith('delete-'))

    def test_relacion_producto_marca_categoria(self):
        self.assertEqual(self.producto.marca, self.marca)
        self.assertEqual(self.producto.categoria, self.categoria)
        self.assertIn(self.producto, self.marca.productos.all())
        self.assertIn(self.producto, self.categoria.productos.all())

    def test_listar_productos_activos_no_incluye_inactivos(self):
        productos_activos = Producto.objects.filter(is_active=True)
        self.assertIn(self.producto, productos_activos)
        self.assertNotIn(self.producto_inactivo, productos_activos)


class CatalogoAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        grupo_vendedor, _ = Group.objects.get_or_create(name='Vendedor')
        grupo_cliente, _ = Group.objects.get_or_create(name='Cliente')

        self.vendedor = UsuarioPersonalizado.objects.create_user(
            username='vendedor1', password='testpass123', email='vendedor@test.com'
        )
        self.vendedor.groups.add(grupo_vendedor)

        self.cliente = UsuarioPersonalizado.objects.create_user(
            username='cliente1', password='testpass123', email='cliente@test.com'
        )
        self.cliente.groups.add(grupo_cliente)

        self.superuser = UsuarioPersonalizado.objects.create_superuser(
            username='admin', password='adminpass123', email='admin@test.com'
        )

        self.categoria = Categoria.objects.create(
            nombre='Electrodomésticos', descripcion='Productos eléctricos'
        )
        self.marca = Marca.objects.create(
            nombre='Samsung', pais_origen='Corea del Sur'
        )
        self.producto = Producto.objects.create(
            nombre='Televisor',
            sku='TV-001',
            precio_lista=500.00,
            precio_oferta=450.00,
            stock_total=10,
            marca=self.marca,
            categoria=self.categoria,
        )
        self.producto_inactivo = Producto.objects.create(
            nombre='Televisor Viejo',
            sku='TV-002',
            precio_lista=300.00,
            stock_total=0,
            marca=self.marca,
            categoria=self.categoria,
            is_active=False,
        )
        self.proveedor = Proveedor.objects.create(
            nombre='Tech Distribuidor', cuit='20-12345678-9'
        )

    def _auth(self, user):
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_productos_publico_sin_token(self):
        response = self.client.get('/api/catalogo/producto/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_get_producto_get_publico_sin_token(self):
        response = self.client.get('/api/catalogo/producto-get/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_producto_sin_token_devuelve_401(self):
        data = {
            'nombre': 'Nuevo Producto',
            'sku': 'NP-001',
            'precio_lista': '100.00',
            'stock_total': 5,
            'marca': self.marca.id,
            'categoria': self.categoria.id,
        }
        response = self.client.post('/api/catalogo/producto/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_producto_con_vendedor_devuelve_201(self):
        self._auth(self.vendedor)
        data = {
            'nombre': 'Nuevo Producto',
            'sku': 'NP-001',
            'precio_lista': '100.00',
            'stock_total': 5,
            'marca': self.marca.id,
            'categoria': self.categoria.id,
        }
        response = self.client.post('/api/catalogo/producto/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_producto_con_cliente_devuelve_403(self):
        self._auth(self.cliente)
        data = {
            'nombre': 'Nuevo Producto',
            'sku': 'NP-002',
            'precio_lista': '100.00',
            'stock_total': 5,
            'marca': self.marca.id,
            'categoria': self.categoria.id,
        }
        response = self.client.post('/api/catalogo/producto/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_eliminado_logico_producto(self):
        self._auth(self.vendedor)
        response = self.client.post(
            f'/api/catalogo/producto/{self.producto.id}/eliminado_logico/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producto.refresh_from_db()
        self.assertFalse(self.producto.is_active)

    def test_get_producto_detalle(self):
        response = self.client.get(f'/api/catalogo/producto/{self.producto.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Televisor')

    def test_producto_get_anida_marca_categoria_imagenes(self):
        response = self.client.get(f'/api/catalogo/producto-get/{self.producto.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('marca', response.data)
        self.assertIn('categoria', response.data)
        self.assertEqual(response.data['marca']['nombre'], 'Samsung')
        self.assertEqual(response.data['categoria']['nombre'], 'Electrodomésticos')

    def test_filtrar_producto_por_marca(self):
        response = self.client.get(f'/api/catalogo/producto/?marca={self.marca.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertEqual(item['marca'], self.marca.id)

    def test_filtrar_producto_por_categoria(self):
        response = self.client.get(f'/api/catalogo/producto/?categoria={self.categoria.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertEqual(item['categoria'], self.categoria.id)

    def test_buscar_producto_por_nombre(self):
        response = self.client.get('/api/catalogo/producto/?search=Televisor')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_buscar_producto_por_sku(self):
        response = self.client.get('/api/catalogo/producto/?search=TV-001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_listar_productos_no_incluye_inactivos(self):
        response = self.client.get('/api/catalogo/producto/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        skus = [item['sku'] for item in response.data['results']]
        self.assertNotIn('TV-002', skus)

    def test_get_categorias_publico(self):
        response = self.client.get('/api/catalogo/categoria/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_categoria_con_vendedor(self):
        self._auth(self.vendedor)
        data = {'nombre': 'Nueva Categoría', 'descripcion': 'Test'}
        response = self.client.post('/api/catalogo/categoria/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_marcas_publico(self):
        response = self.client.get('/api/catalogo/marca/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_proveedores_requiere_autenticacion(self):
        response = self.client.get('/api/catalogo/proveedor/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_proveedores_con_vendedor(self):
        self._auth(self.vendedor)
        response = self.client.get('/api/catalogo/proveedor/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtener_jwt_token(self):
        response = self.client.post(
            '/api/token/',
            {'username': 'vendedor1', 'password': 'testpass123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_jwt_token(self):
        obtain_response = self.client.post(
            '/api/token/',
            {'username': 'vendedor1', 'password': 'testpass123'},
            format='json'
        )
        refresh_token = obtain_response.data['refresh']
        response = self.client.post(
            '/api/token/refresh/',
            {'refresh': refresh_token},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_paginacion_producto_get(self):
        for i in range(15):
            Producto.objects.create(
                nombre=f'Producto {i}',
                sku=f'SKU-{i:03d}',
                precio_lista=100.00,
                stock_total=1,
                marca=self.marca,
                categoria=self.categoria,
            )
        response = self.client.get('/api/catalogo/producto-get/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 10)

    def test_eliminado_logico_proveedor(self):
        self._auth(self.vendedor)
        response = self.client.post(
            f'/api/catalogo/proveedor/{self.proveedor.id}/eliminado_logico/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.proveedor.refresh_from_db()
        self.assertFalse(self.proveedor.is_active)