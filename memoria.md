# MEMORIA — Proyecto NexusGamer (Django REST)

## Estado actual del proyecto

Ubicación: `/home/maxi/Documents/ingenieriasoftware/djangorest/efi2_ing_soft`

Rama activa: `main` (commits: `d543c52`, `2c93380`, `a8c2158`)

Archivos SQL existentes (referencia, no se modificaron):
- `nexusgamer_schema.sql` (~17 tablas: catalogo_*, wishlist_*)
- `nexusgamer_postgres.sql` (~30 tablas: catalogo_*, carrito_*, ordenes_*, promociones_*, pagos_*, envios_*, wishlist_*, reviews_*)

## Qué se hizo en esta sesión

### 1. Creación de la app `catalogo`
Comando: `python manage.py startapp catalogo`

Estructura generada:
```
catalogo/
  __init__.py
  admin.py
  apps.py        -> CatalogoConfig (name = 'catalogo')
  migrations/
  models.py      -> LLENADO con modelos de catalogo_*
  tests.py
  views.py       -> LLENADO con 11 ModelViewSet
  urls.py        -> CREADO con DefaultRouter (11 endpoints)
```

### 2. Registro en settings
Archivo: `settings/settings.py`

Se agregó `'catalogo'` a `INSTALLED_APPS`.

### 3. Modelos (`catalogo/models.py`)
Basados en `nexusgamer_postgres.sql`. 11 modelos con `db_table` coincidente:

| Modelo | Tabla SQL | Relaciones clave |
|--------|-----------|------------------|
| `Categoria` | `catalogo_categoria` | autoreferencial (`categoria_padre`) |
| `Marca` | `catalogo_marca` | — |
| `Producto` | `catalogo_producto` | FK Marca, FK Categoría |
| `ProductoImagen` | `catalogo_productoimagen` | FK Producto (CASCADE) |
| `Especificacion` | `catalogo_especificacion` | FK Producto (CASCADE) |
| `Variante` | `catalogo_variante` | FK Producto (CASCADE) |
| `Compatibilidad` | `catalogo_compatibilidad` | FK Producto x2 (origen/destino) |
| `Etiqueta` | `catalogo_etiqueta` | — |
| `ProductoEtiqueta` | `catalogo_producto_etiqueta` | FK Producto, FK Etiqueta (M2M intermedio) |
| `Proveedor` | `catalogo_proveedor` | — |
| `Compra` | `catalogo_compra` | FK Proveedor |

Campos destacados: `BigAutoField` (BIGSERIAL), `JSONField` (atributos), `SlugField` único, `DecimalField` con checks, `BooleanField` para estados, `DateTimeField` con `auto_now_add` / `auto_now`.

### 4. Serializers (`catalogo/serializers.py`)
Serializers para todos los modelos. Validaciones incluidas:
- `ProductoImagenSerializer`: solo una imagen `es_principal=True` por producto
- `VarianteSerializer`: `stock >= 0`
- `CompatibilidadSerializer`: un producto no puede ser compatible consigo mismo
- `CompraSerializer`: `total >= 0`
- `ProductoSerializer`: `precio_oferta <= precio_lista`

Nested serializers (anidados solo en list):
- `CategoriaSerializer`: campo `subcategorias` (vacío si se consulta detalle con `pk`, lleno en list)
- `ProductoSerializer`: campos planos (FKs por ID)
- `ProductoListSerializer` (hereda de ProductoSerializer): anida `marca`, `categoria`, `imagenes`, `especificaciones`, `variantes`

### 5. Views (`catalogo/views.py`)
11 `ModelViewSet` (uno por modelo) con queryset y serializer_class definidos.
`ProductoViewSet` sobrescribe `get_serializer_class()`: usa `ProductoListSerializer` en `list`, `ProductoSerializer` en el resto.

### 6. URLs (`catalogo/urls.py` + `settings/urls.py`)
`catalogo/urls.py`: `DefaultRouter` con 11 registros:
```
categorias, marcas, productos, producto-imagenes, especificaciones,
variantes, compatibilidades, etiquetas, producto-etiquetas, proveedores, compras
```

`settings/urls.py`: agregado `path('api/catalogo/', include('catalogo.urls'))`.

### 7. Verificación
- `python -m py_compile` en archivos nuevos: OK
- `python manage.py check`: 0 issues
- Import de serializers y router vía `manage.py shell`: OK

## Lo que falta (según requisitos.md)

### Instalación y dependencias
- [ ] Gestor `uv` + `pyproject.toml` / `requirements.txt`
- [ ] `djangorestframework`, `django-cors-headers`, `drf-spectacular` (swagger/redoc), `django-filter`, `psycopg2-binary`

### Configuración de settings
- [ ] Base de datos PostgreSQL (en lugar de SQLite)
- [ ] CORS configurado para frontend
- [ ] Autenticación Session + Token
- [ ] Paginación por defecto en get all
- [ ] Filtros y búsquedas (`DjangoFilterBackend`, `SearchFilter`)
- [ ] API navegable de DRF habilitada

### API REST
- [ ] Al menos 8 de 10 modelos con endpoint ViewSet (ya hay 11, falta configurar auth/paginación/filtros)
- [ ] Al menos 2 CRUD ViewSets con `NestedSerializers` solo en `list` (solo Producto lo tiene por ahora; falta un segundo, ej. Marca con productos anidados o Categoria con subcategorías)
- [ ] Al menos 2 funciones con decorador `@action` personalizadas
- [ ] Endpoints protegidos según corresponda (Session y Token)
- [ ] Documentación OpenAPI/Swagger/Redoc (`drf-spectacular`)

### Vistas y Admin
- [ ] Vista principal con template de bienvenida
- [ ] `admin.py` con modelos registrados, filtros, ordenamiento y búsqueda

### Docker
- [ ] `Dockerfile`
- [ ] `docker-compose.yml` (Django + Postgres)

### Git y README
- [ ] Commits descriptivos por funcionalidad
- [ ] `README.md` con arquitectura, diagrama de tablas, instrucciones y capturas del proyecto funcionando
- [ ] Última versión en rama `main`/`master`

## Próximos pasos sugeridos
1. Instalar dependencias con `uv` y configurar `settings.py` (Postgre, DRF, CORS, auth, paginación, filtros, spectacular).
2. Crear `Dockerfile` y `docker-compose.yml`.
3. Agregar autenticación y proteger endpoints.
4. Agregar segundo ViewSet con nested serializers solo en list.
5. Agregar al menos 2 métodos `@action`.
6. Configurar `admin.py` y vista de bienvenida.
7. Documentar en `README.md`.
