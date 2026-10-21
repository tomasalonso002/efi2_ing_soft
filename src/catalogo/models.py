from django.db import models


class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False)
    slug = models.SlugField(max_length=200, unique=True, null=False)
    descripcion = models.TextField(blank=True, null=True)
    imagen_url = models.CharField(max_length=500, blank=True, null=True)
    categoria_padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategorias',
        db_column='categoria_padre_id',
    )
    orden = models.IntegerField(default=0, null=False)
    activa = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'catalogo_categoria'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False)
    slug = models.SlugField(max_length=200, unique=True, null=False)
    logo_url = models.CharField(max_length=500, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    pais_origen = models.CharField(max_length=100, blank=True, null=True)
    activa = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'catalogo_marca'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=200, null=False)
    slug = models.SlugField(max_length=250, unique=True, null=False)
    descripcion_corta = models.CharField(max_length=500, blank=True, null=True)
    descripcion_larga = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True, null=False)
    precio_lista = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    precio_oferta = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    iva_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2, default=21.00, null=False
    )
    stock_total = models.IntegerField(default=0, null=False)
    stock_reservado = models.IntegerField(default=0, null=False)
    activo = models.BooleanField(default=True, null=False)
    destacado = models.BooleanField(default=False, null=False)
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        null=False,
        related_name='productos',
        db_column='marca_id',
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        null=False,
        related_name='productos',
        db_column='categoria_id',
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'catalogo_producto'
        ordering = ['-created_at']

    def __str__(self):
        return self.nombre


class ProductoImagen(models.Model):
    id = models.BigAutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        null=False,
        related_name='imagenes',
        db_column='producto_id',
    )
    imagen_url = models.CharField(max_length=500, null=False)
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    orden = models.IntegerField(default=0, null=False)
    es_principal = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'catalogo_productoimagen'
        ordering = ['orden', 'id']

    def __str__(self):
        return f'Imagen de {self.producto.nombre}'


class Especificacion(models.Model):
    TIPO_CHOICES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('boolean', 'Boolean'),
    ]

    id = models.BigAutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        null=False,
        related_name='especificaciones',
        db_column='producto_id',
    )
    nombre = models.CharField(max_length=150, null=False)
    valor = models.CharField(max_length=500, null=False)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='text', null=False)
    unidad = models.CharField(max_length=50, blank=True, null=True)
    orden = models.IntegerField(default=0, null=False)

    class Meta:
        db_table = 'catalogo_especificacion'
        ordering = ['orden', 'id']

    def __str__(self):
        return f'{self.nombre}: {self.valor}'


class Variante(models.Model):
    id = models.BigAutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        null=False,
        related_name='variantes',
        db_column='producto_id',
    )
    sku_variante = models.CharField(max_length=100, unique=True, null=False)
    nombre = models.CharField(max_length=200, null=False)
    precio_adicional = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, null=False
    )
    stock = models.IntegerField(default=0, null=False)
    activa = models.BooleanField(default=True, null=False)
    atributos = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'catalogo_variante'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.producto.nombre} - {self.nombre}'


class Compatibilidad(models.Model):
    id = models.BigAutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        null=False,
        related_name='compatibilidades_origen',
        db_column='producto_id',
    )
    producto_compatible = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        null=False,
        related_name='compatibilidades_destino',
        db_column='producto_compatible_id',
    )
    tipo_compatibilidad = models.CharField(max_length=50, null=False)
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'catalogo_compatibilidad'
        unique_together = [['producto', 'producto_compatible', 'tipo_compatibilidad']]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.producto.nombre} compatible con {self.producto_compatible.nombre}'


class Etiqueta(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True, null=False)
    slug = models.SlugField(max_length=50, unique=True, null=False)
    color_hex = models.CharField(max_length=7, default='#000000', null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'catalogo_etiqueta'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class ProductoEtiqueta(models.Model):
    id = models.BigAutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        null=False,
        related_name='producto_etiquetas',
        db_column='producto_id',
    )
    etiqueta = models.ForeignKey(
        Etiqueta,
        on_delete=models.CASCADE,
        null=False,
        related_name='producto_etiquetas',
        db_column='etiqueta_id',
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'catalogo_producto_etiqueta'
        unique_together = [['producto', 'etiqueta']]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.producto.nombre} - {self.etiqueta.nombre}'


class Proveedor(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False)
    cuit = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'catalogo_proveedor'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('recibida', 'Recibida'),
        ('cancelada', 'Cancelada'),
    ]

    id = models.BigAutoField(primary_key=True)
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        null=False,
        related_name='compras',
        db_column='proveedor_id',
    )
    fecha_compra = models.DateTimeField(auto_now_add=True, null=False)
    total = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='pendiente', null=False
    )
    nro_factura = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'catalogo_compra'
        ordering = ['-fecha_compra']

    def __str__(self):
        return f'Compra {self.id} - {self.proveedor.nombre}'
