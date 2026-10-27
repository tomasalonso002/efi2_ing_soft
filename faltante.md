# Faltantes para cumplir requisitos.md

## Estado general
Se revisó `requisitos.md` y se comparó con el proyecto actual. La paginación ya se implementó. Quedan los siguientes faltantes:

---

## 1. Base de datos

| Requisito | Estado |
|-----------|--------|
| Al menos 10 modelos | ✅ Cumplido (11 modelos) |
| Modelos relevantes | ✅ Cumplido |
| Relaciones entre modelos | ✅ Cumplido |
| Planificación de tablas y relaciones en README | ❌ Faltante |

**Acción:** Agregar diagrama o descripción escrita de la planificación de tablas y relaciones en `README.md`.

---

## 2. API REST

| Requisito | Estado |
|-----------|--------|
| API REST para frontend | ✅ Cumplido |
| Al menos 8 modelos con ViewSet | ✅ Cumplido (los 11) |
| Al menos 2 Viewsets CRUD con NestedSerializers en list | ⚠️ Parcial (solo `ProductoListSerializer` anida marca/categoria/imagenes; falta un segundo) |
| Endpoints protegidos con Sesión y Tokens | ⚠️ Parcial (JWT configurado; verificar Sesión) |
| Al menos 2 funciones @action | ✅ Cumplido (`eliminado_logico` en todos los ModelViewSet) |
| Get all con paginación | ✅ Cumplido |
| Al menos 1 viewset con filtros y búsquedas | ✅ Cumplido (`ProductoViewSet` con DjangoFilterBackend, SearchFilter, OrderingFilter) |
| Documentación OpenAPI/Swagger/Redoc + API navegable | ⚠️ Parcial (API navegable por defecto de DRF; Swagger/OpenAPI lo maneja otro compañero) |

**Acciones:**
- ✅ Agregar `search_fields`, `filterset_fields` o `DjangoFilterBackend` en al menos un ViewSet (`ProductoViewSet`).
- Instalar y configurar `drf-spectacular` (o similar) para generar documentación OpenAPI/Swagger/Redoc (pendiente, otro compañero).
- Crear un segundo serializer con datos anidados solo para el listado (ej: `CompraListSerializer` anidando proveedor y detalles).

---

## 3. Vistas

| Requisito | Estado |
|-----------|--------|
| Vista principal con template de bienvenida | ❌ Faltante |
| Panel de administración con filtros, ordenamiento y búsqueda | ❌ Faltante |

**Acciones:**
- Crear una vista basada en función o clase que renderice un template HTML de bienvenida (no requiere CRUD por formularios).
- Crear `ModelAdmin` personalizado en `admin.py` para los modelos relevantes con `list_filter`, `search_fields` y `ordering`.

---

## 4. Otros requisitos

| Requisito | Estado |
|-----------|--------|
| `uv` como gestor de entornos virtuales | ❓ No verificado |
| CORS configurado para frontend | ❓ No verificado |
| Proyecto dockerizado | ❓ No verificado |
| Git organizado (ramas, PRs, commits descriptivos) | ⚠️ Parcial |

**Acciones:**
- Verificar e instalar `uv` si no se usa.
- Agregar `django-cors-headers` y configurar `CORS_ALLOWED_ORIGINS` en `settings.py`.
- Crear `Dockerfile` y `docker-compose.yml` para dockerizar el proyecto.
- Organizar trabajo en Git con ramas, pull requests y commits descriptivos.

---

## 5. Entrega

| Requisito | Estado |
|-----------|--------|
| Repositorio GitHub en rama main/master | ⚠️ Parcial (pendiente de subir) |
| README.md con capturas del proyecto | ❌ Faltante |

**Acciones:**
- Subir el proyecto a GitHub en la rama `main` o `master`.
- Crear `README.md` con descripción, capturas del proyecto en funcionamiento, instrucciones de instalación y uso.

---

## Orden sugerido para implementar

1. ✅ Filtros y búsquedas en al menos un ViewSet (`ProductoViewSet` completado)
2. Documentación Swagger/OpenAPI (drf-spectacular) — pendiente, otro compañero
3. Vista principal con template de bienvenida — descartado
4. ModelAdmin personalizado en admin
5. Segundo NestedSerializer con datos anidados en list
6. CORS, Docker, `uv` (verificar/configurar)
7. README.md con capturas y subir a GitHub

---