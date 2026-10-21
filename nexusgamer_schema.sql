-- ============================================================
-- NEXUSGAMER - Esquema SQL para PostgreSQL
-- Alineado con los modelos de Django (apps: catalogo, wishlist)
-- ============================================================

-- ============================================================
-- 1. CATALOGO (Base)
-- ============================================================

-- Tabla: catalogo_categoria
CREATE TABLE catalogo_categoria (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    imagen_url VARCHAR(500),
    categoria_padre_id BIGINT REFERENCES catalogo_categoria(id) ON DELETE SET NULL,
    orden INTEGER DEFAULT 0 NOT NULL,
    activa BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_catalogo_categoria_slug ON catalogo_categoria(slug);
CREATE INDEX idx_catalogo_categoria_padre_id ON catalogo_categoria(categoria_padre_id);
CREATE INDEX idx_catalogo_categoria_activa ON catalogo_categoria(activa);
CREATE INDEX idx_catalogo_categoria_orden ON catalogo_categoria(orden);

-- Tabla: catalogo_marca
CREATE TABLE catalogo_marca (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    logo_url VARCHAR(500),
    descripcion TEXT,
    pais_origen VARCHAR(100),
    activa BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_catalogo_marca_slug ON catalogo_marca(slug);
CREATE INDEX idx_catalogo_marca_activa ON catalogo_marca(activa);

-- Tabla: catalogo_producto
CREATE TABLE catalogo_producto (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    descripcion_corta TEXT,
    descripcion_larga TEXT,
    sku VARCHAR(50) UNIQUE NOT NULL,
    precio_lista NUMERIC(12, 2) NOT NULL CHECK (precio_lista >= 0),
    precio_oferta NUMERIC(12, 2) CHECK (precio_oferta >= 0),
    iva_porcentaje NUMERIC(5, 2) DEFAULT 21.00 NOT NULL CHECK (iva_porcentaje >= 0 AND iva_porcentaje <= 100),
    stock_total INTEGER DEFAULT 0 NOT NULL CHECK (stock_total >= 0),
    stock_reservado INTEGER DEFAULT 0 NOT NULL CHECK (stock_reservado >= 0),
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    destacado BOOLEAN DEFAULT FALSE NOT NULL,
    fecha_lanzamiento TIMESTAMPTZ,
    marca_id BIGINT REFERENCES catalogo_marca(id) ON DELETE RESTRICT,
    categoria_id BIGINT REFERENCES catalogo_categoria(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_catalogo_producto_slug ON catalogo_producto(slug);
CREATE INDEX idx_catalogo_producto_sku ON catalogo_producto(sku);
CREATE INDEX idx_catalogo_producto_marca_id ON catalogo_producto(marca_id);
CREATE INDEX idx_catalogo_producto_categoria_id ON catalogo_producto(categoria_id);
CREATE INDEX idx_catalogo_producto_activo ON catalogo_producto(activo);
CREATE INDEX idx_catalogo_producto_destacado ON catalogo_producto(destacado);
CREATE INDEX idx_catalogo_producto_fecha_lanzamiento ON catalogo_producto(fecha_lanzamiento);
CREATE INDEX idx_catalogo_producto_precio_lista ON catalogo_producto(precio_lista);

-- Tabla: catalogo_productoimagen
CREATE TABLE catalogo_productoimagen (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    imagen_url VARCHAR(500) NOT NULL,
    alt_text VARCHAR(200),
    orden INTEGER DEFAULT 0 NOT NULL,
    es_principal BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_catalogo_productoimagen_producto_id ON catalogo_productoimagen(producto_id);
CREATE INDEX idx_catalogo_productoimagen_orden ON catalogo_productoimagen(orden);
CREATE INDEX idx_catalogo_productoimagen_es_principal ON catalogo_productoimagen(es_principal);

-- Tabla: catalogo_especificacion
CREATE TABLE catalogo_especificacion (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    valor VARCHAR(255) NOT NULL,
    tipo VARCHAR(10) DEFAULT 'text' NOT NULL CHECK (tipo IN ('text', 'number', 'boolean')),
    unidad VARCHAR(50),
    orden INTEGER DEFAULT 0 NOT NULL
);

CREATE INDEX idx_catalogo_especificacion_producto_id ON catalogo_especificacion(producto_id);
CREATE INDEX idx_catalogo_especificacion_nombre ON catalogo_especificacion(nombre);
CREATE INDEX idx_catalogo_especificacion_orden ON catalogo_especificacion(orden);

-- Tabla: catalogo_variante
CREATE TABLE catalogo_variante (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    sku_variante VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio_adicional NUMERIC(12, 2) DEFAULT 0.00 NOT NULL CHECK (precio_adicional >= 0),
    stock INTEGER DEFAULT 0 NOT NULL CHECK (stock >= 0),
    activa BOOLEAN DEFAULT TRUE NOT NULL,
    atributos JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_catalogo_variante_producto_id ON catalogo_variante(producto_id);
CREATE INDEX idx_catalogo_variante_sku ON catalogo_variante(sku_variante);
CREATE INDEX idx_catalogo_variante_activa ON catalogo_variante(activa);
CREATE INDEX idx_catalogo_variante_atributos_gin ON catalogo_variante USING GIN(atributos);

-- ============================================================
-- 2. WISHLIST (Requiere que auth_user ya exista)
-- ============================================================

CREATE TABLE wishlist_listadeseos (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT UNIQUE NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    creado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    actualizado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE UNIQUE INDEX idx_wishlist_listadeseos_usuario_id ON wishlist_listadeseos(usuario_id);

CREATE TABLE wishlist_item (
    id BIGSERIAL PRIMARY KEY,
    lista_id BIGINT NOT NULL REFERENCES wishlist_listadeseos(id) ON DELETE CASCADE,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    variante_id BIGINT REFERENCES catalogo_variante(id) ON DELETE CASCADE,
    agregado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_wishlist_item_lista_id ON wishlist_item(lista_id);
CREATE INDEX idx_wishlist_item_producto_id ON wishlist_item(producto_id);
CREATE INDEX idx_wishlist_item_variante_id ON wishlist_item(variante_id);
CREATE UNIQUE INDEX idx_wishlist_item_lista_producto_variante_unique ON wishlist_item(lista_id, producto_id, variante_id);

-- ============================================================
-- 3. COMPATIBILIDAD DE COMPONENTES
-- ============================================================

CREATE TABLE catalogo_compatibilidad (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    producto_compatible_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    tipo_compatibilidad VARCHAR(50) NOT NULL,
    notas TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    CHECK (producto_id != producto_compatible_id),
    UNIQUE(producto_id, producto_compatible_id, tipo_compatibilidad)
);

CREATE INDEX idx_catalogo_compatibilidad_producto ON catalogo_compatibilidad(producto_id);
CREATE INDEX idx_catalogo_compatibilidad_compatible ON catalogo_compatibilidad(producto_compatible_id);
CREATE INDEX idx_catalogo_compatibilidad_tipo ON catalogo_compatibilidad(tipo_compatibilidad);

-- ============================================================
-- 4. RESEÑAS DE PRODUCTOS (Requiere auth_user)
-- ============================================================

CREATE TABLE catalogo_resena (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    usuario_id BIGINT NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    calificacion SMALLINT NOT NULL CHECK (calificacion >= 1 AND calificacion <= 5),
    comentario TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    UNIQUE(producto_id, usuario_id)
);

CREATE INDEX idx_catalogo_resena_producto_id ON catalogo_resena(producto_id);
CREATE INDEX idx_catalogo_resena_usuario_id ON catalogo_resena(usuario_id);
CREATE INDEX idx_catalogo_resena_calificacion ON catalogo_resena(calificacion);

-- ============================================================
-- 5. ETIQUETAS DE PRODUCTOS
-- ============================================================

CREATE TABLE catalogo_etiqueta (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    color_hex VARCHAR(7) DEFAULT '#000000' CHECK (color_hex ~ '^#[0-9A-Fa-f]{6}$'),
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_catalogo_etiqueta_slug ON catalogo_etiqueta(slug);

CREATE TABLE catalogo_producto_etiqueta (
    id BIGSERIAL PRIMARY KEY,
    producto_id BIGINT NOT NULL REFERENCES catalogo_producto(id) ON DELETE CASCADE,
    etiqueta_id BIGINT NOT NULL REFERENCES catalogo_etiqueta(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    UNIQUE(producto_id, etiqueta_id)
);

CREATE INDEX idx_catalogo_producto_etiqueta_prod ON catalogo_producto_etiqueta(producto_id);
CREATE INDEX idx_catalogo_producto_etiqueta_etq ON catalogo_producto_etiqueta(etiqueta_id);

-- ============================================================
-- 6. PROVEEDORES Y COMPRAS
-- ============================================================

CREATE TABLE catalogo_proveedor (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    cuit VARCHAR(20) UNIQUE,
    email VARCHAR(150),
    telefono VARCHAR(50),
    direccion TEXT,
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_catalogo_proveedor_nombre ON catalogo_proveedor(nombre);
CREATE INDEX idx_catalogo_proveedor_cuit ON catalogo_proveedor(cuit);

CREATE TABLE catalogo_compra (
    id BIGSERIAL PRIMARY KEY,
    proveedor_id BIGINT NOT NULL REFERENCES catalogo_proveedor(id) ON DELETE RESTRICT,
    fecha_compra TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    total NUMERIC(12, 2) NOT NULL CHECK (total >= 0),
    estado VARCHAR(20) DEFAULT 'pendiente' NOT NULL CHECK (estado IN ('pendiente', 'recibida', 'cancelada')),
    nro_factura VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_catalogo_compra_proveedor ON catalogo_compra(proveedor_id);
CREATE INDEX idx_catalogo_compra_estado ON catalogo_compra(estado);

-- ============================================================
-- TRIGGERS PARA updated_at
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_catalogo_categoria_updated_at
    BEFORE UPDATE ON catalogo_categoria
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER tr_catalogo_marca_updated_at
    BEFORE UPDATE ON catalogo_marca
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER tr_catalogo_producto_updated_at
    BEFORE UPDATE ON catalogo_producto
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER tr_catalogo_variante_updated_at
    BEFORE UPDATE ON catalogo_variante
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER tr_wishlist_listadeseos_updated_at
    BEFORE UPDATE ON wishlist_listadeseos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER tr_catalogo_resena_updated_at
    BEFORE UPDATE ON catalogo_resena
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER tr_catalogo_proveedor_updated_at
    BEFORE UPDATE ON catalogo_proveedor
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- DATOS SEMILLA MÍNIMOS
-- ============================================================

-- Categorías raíz ejemplo
INSERT INTO catalogo_categoria (nombre, slug, descripcion, orden, activa) VALUES
('Hardware', 'hardware', 'Componentes de PC', 1, TRUE),
('Periféricos', 'perifericos', 'Periféricos y accesorios', 2, TRUE),
('Consolas', 'consolas', 'Consolas de videojuegos', 3, TRUE),
('Monitores', 'monitores', 'Monitores y displays', 4, TRUE),
('Sillas Gaming', 'sillas-gaming', 'Sillas ergonómicas para gaming', 5, TRUE)
ON CONFLICT (slug) DO NOTHING;

-- Marcas ejemplo
INSERT INTO catalogo_marca (nombre, slug, descripcion, pais_origen, activa) VALUES
('NVIDIA', 'nvidia', 'Tarjetas gráficas NVIDIA', 'USA', TRUE),
('AMD', 'amd', 'Procesadores y GPUs AMD', 'USA', TRUE),
('ASUS', 'asus', 'Hardware gaming', 'Taiwan', TRUE),
('MSI', 'msi', 'Hardware gaming', 'Taiwan', TRUE),
('Logitech', 'logitech', 'Periféricos gaming', 'Suiza', TRUE),
('Razer', 'razer', 'Periféricos gaming', 'USA', TRUE)
ON CONFLICT (slug) DO NOTHING;

-- Etiquetas ejemplo
INSERT INTO catalogo_etiqueta (nombre, slug, color_hex) VALUES
('Oferta', 'oferta', '#FF0000'),
('Nuevo Ingreso', 'nuevo-ingreso', '#00FF00'),
('Gamer', 'gamer', '#800080'),
('Oficina', 'oficina', '#0000FF'),
('Reacondicionado', 'reacondicionado', '#FFA500'),
('Envío Gratis', 'envio-gratis', '#008000')
ON CONFLICT (slug) DO NOTHING;

-- Proveedores de prueba
INSERT INTO catalogo_proveedor (nombre, cuit, email) VALUES
('Distribuidora Tech S.A.', '30-12345678-9', 'ventas@techsa.com'),
('Mayorista Gamer SRL', '30-98765432-1', 'compras@mayoristagamer.com')
ON CONFLICT (cuit) DO NOTHING;

-- ============================================================
-- FIN DEL ESQUEMA
-- ============================================================
