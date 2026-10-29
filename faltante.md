# Faltantes para cumplir requisitos.md

## Estado general

Se revisó `requisitos.md` y se comparó con el proyecto actual. Los siguientes requisitos están **cumplidos** o **pendientes**:

---

## 1. Base de datos

| Requisito | Estado |
|-----------|--------|
| Al menos 10 modelos | ✅ Cumplido (10 modelos) |
| Modelos relevantes | ✅ Cumplido |
| Relaciones entre modelos | ✅ Cumplido |
| Planificación de tablas y relaciones en README | ✅ Cumplido (sección agregada en README.md) |

---

## 2. API REST

| Requisito | Estado |
|-----------|--------|
| API REST para frontend | ✅ Cumplido |
| Al menos 8 modelos con ViewSet | ✅ Cumplido (los 10) |
| Al menos 2 Viewsets CRUD con NestedSerializers en list | ✅ Cumplido (`ProductoListSerializer`, `CompraListSerializer`) |
| Endpoints protegidos con Sesión y Tokens | ✅ Cumplido (JWT + SessionAuthentication) |
| Al menos 2 funciones @action | ✅ Cumplido (`eliminado_logico` en todos los ModelViewSet) |
| Get all con paginación | ✅ Cumplido (PageNumberPagination, PAGE_SIZE=10) |
| Al menos 1 viewset con filtros y búsquedas | ✅ Cumplido (`ProductoViewSet`) |
| Documentación OpenAPI/Swagger/Redoc + API navegable | ✅ Cumplido (drf-spectacular configurado, DRF API navegable por defecto) |

---

## 3. Vistas

| Requisito | Estado |
|-----------|--------|
| Vista principal con template de bienvenida | ✅ Cumplido (`inicio` + `inicio.html`) |
| Panel de administración con filtros, ordenamiento y búsqueda | ✅ Cumplido (todas las apps tienen ModelAdmin) |

---

## 4. Otros requisitos

| Requisito | Estado |
|-----------|--------|
| `uv` como gestor de entornos virtuales | ✅ Cumplido (`pyproject.toml`, `uv.lock`) |
| CORS configurado para frontend | ✅ Cumplido (`django-cors-headers`, `CORS_ALLOWED_ORIGINS`) |
| Proyecto dockerizado | ✅ Cumplido (`Dockerfile`, `compose.yaml`) |
| Git organizado (ramas, PRs, commits descriptivos) | ✅ Cumplido (ramas main, develope, max, tomas) |

---

## 5. Entrega

| Requisito | Estado |
|-----------|--------|
| Repositorio GitHub en rama main/master | ⚠️ Pendiente (última versión en `develope`, falta merge a `main`) |
| README.md con capturas del proyecto | ❌ Faltante (no hay capturas disponibles) |

---

## Acciones pendientes

1. Fusionar `develope` → `main` (no subir a GitHub si no se solicita).
2. Agregar capturas del proyecto al README.md (si se dispusieran).

---

## Correcciones aplicadas en esta sesión

- `src/usuarios/views.py`: Corregido `eliminado_logico` de `ListaDeseosProductosPostViewSets` (ya no referencia `producto.nombre`, campo inexistente).
- `pyproject.toml`: `requires-python` de `>=3.14` a `>=3.10`; `django` de `>=6.1.2` a `>=5.0,<6.0`; removido duplicado `django-filter`.
- `src/usuarios/admin.py`: Agregados `ModelAdmin` con `list_filter`, `search_fields`, `ordering` para `UsuarioPersonalizado` y `ListaDeseosProductos`.
- `src/usuarios/templates/usuarios/inicio.html`: Enlaces rotos corregidos (`/api/compra/` → `/api/compras/`, `/api/venta/` → `/api/ventas/`).
- `README.md`: Agregada sección "Planificación de tablas y relaciones"; sección "Pendientes" actualizada.
- `memoria.md`: Sección "Lo que falta" actualizada (Swagger/CORS/Docker ya configurados); notas importantes actualizadas.
