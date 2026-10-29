# efi2_ing_soft

Sistema de gestión de tienda de productos de computación con API REST construida en Django REST Framework.

## Librerías instaladas

- django-filter
- djangorestframework-simplejwt
- Pillow
- drf-spectacular
- django-cors-headers

## Estructura del proyecto

```
src/
├── usuarios/         # UsuarioPersonalizado, ListaDeseosProductos
├── catalogo/         # Categoria, Marca, Producto
├── proveedores/      # Proveedor
├── compras/          # Compra, DetalleCompra
├── ventas/           # Venta, DetalleVenta
├── efi2_ing_soft/    # Configuración Django (settings, urls)
├── manage.py
├── seed_db.py        # Script de siembra de datos
└── db.sqlite3
```

## Modelos (10 total)

| App | Modelos |
|-----|---------|
| usuarios | UsuarioPersonalizado, ListaDeseosProductos |
| catalogo | Categoria, Marca, Producto |
| proveedores | Proveedor |
| compras | Compra, DetalleCompra |
| ventas | Venta, DetalleVenta |

## Planificación de tablas y relaciones

Se planificó la base de datos antes del desarrollo, organizando los modelos en 5 apps según su responsabilidad:

```
Categoria ── Producto ── Marca
                    │
                    ├── DetalleCompra ── Compra ── Proveedor
                    │
                    └── DetalleVenta ── Venta ── Usuario (AUTH_USER_MODEL)
```

Relaciones entre modelos:
- Una `Categoria` tiene muchos `Producto`.
- Una `Marca` tiene muchos `Producto`.
- Un `Producto` pertenece a una `Categoria` y a una `Marca`.
- Un `Proveedor` puede tener muchas `Compra`.
- Una `Compra` tiene muchos `DetalleCompra`; un `DetalleCompra` pertenece a un `Producto`.
- Una `Venta` pertenece a un usuario/cliente y tiene muchos `DetalleVenta`; un `DetalleVenta` pertenece a un `Producto`.
- `ListaDeseosProductos` relaciona un `UsuarioPersonalizado` con un `Producto`.

## Endpoints principales

- `api/usuarios/` — clientes, vendedores, lista de deseos
- `api/catalogo/` — categorías, marcas, productos
- `api/proveedores/` — proveedores
- `api/compras/` — compras y detalles de compra
- `api/ventas/` — ventas y detalles de venta
- `api/token/` — JWT obtain
- `api/token/refresh/` — JWT refresh
- `admin/` — Django admin

## Autenticación

- JWT (access + refresh tokens)
- Sesión (navegador)
- GET público, escritura requiere autenticación de vendedor

## Cómo ejecutar

```bash
# Instalar dependencias
uv sync

# Cargar datos de prueba
uv run python src/seed_db.py

# Ejecutar servidor
uv run python src/manage.py runserver

# Ejecutar tests
uv run python src/manage.py test usuarios catalogo proveedores compras ventas

# Verificar proyecto
uv run python src/manage.py check
```

## Credenciales de prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin | Superusuario |
| vendedor1 | testpass123 | Vendedor |
| cliente1 | testpass123 | Cliente |

## Requisitos cumplidos

- ✅ 10 modelos en la base de datos con relaciones
- ✅ API REST con ViewSets para todos los modelos
- ✅ Endpoints protegidos con JWT y Sesión
- ✅ Al menos 2 funciones @action (eliminado_logico en todos los ModelViewSet)
- ✅ Get all con paginación
- ✅ Filtros y búsquedas en ProductoViewSet
- ✅ Panel de administración con filtros, ordenamiento y búsqueda
- ✅ 2 NestedSerializers con datos anidados en list (ProductoListSerializer, CompraListSerializer)
- ✅ Tests creados y pasando (15 tests)
- ✅ uvc como gestor de entornos (pyproject.toml, uv.lock)

## Pendientes

- ⚠️ README.md con capturas del proyecto en funcionamiento (no disponibles por ahora)
- ⚠️ Fusionar la última versión a la rama `main`/`master` del repositorio de GitHub
