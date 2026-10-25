# efi2_ing_soft

Librerias intaladas:
django-filter
djangorestframework-simplejwt
Pillow
drf-spectacular
django-cors-headers


ENDOPINTS:

**USUARIOS:**

## CLIENTE:
POST:
http://127.0.0.1:8000/api/usuarios/cliente/

JSON:
{
 "username":"martin99",
  "first_name":"Martin",
  "last_name":"Alonso",
  "password":"Itec123@"
}

http://127.0.0.1:8000/api/usuarios/cliente/1/eliminado_logico/

PUT:
http://127.0.0.1:8000/api/usuarios/cliente/1/
JSON:
{
 "username":"martin99"
}

GET:
http://127.0.0.1:8000/api/usuarios/cliente/
http://127.0.0.1:8000/api/usuarios/cliente/1/

## CLIENTE ONLY READ:
GET:
http://127.0.0.1:8000/api/usuarios/cliente-get/
http://127.0.0.1:8000/api/usuarios/cliente-get/1/


## VENDEDOR:
POST:
http://127.0.0.1:8000/api/usuarios/vendedor/

JSON:
{
 "username":"martin99",
  "first_name":"Martin",
  "last_name":"Alonso",
  "password":"Itec123@"
}

http://127.0.0.1:8000/api/usuarios/vendedor/1/eliminado_logico/

PUT:
http://127.0.0.1:8000/api/usuarios/vendedor/1/
JSON:
{
 "username":"martin99"
}

GET:
http://127.0.0.1:8000/api/usuarios/vendedor/
http://127.0.0.1:8000/api/usuarios/vendedor/1/


## VENDEDOR ONLY READ:
GET:
http://127.0.0.1:8000/api/vendedor/categoria-get/
http://127.0.0.1:8000/api/vendedor/categoria-get/2/

**CATALOGO:**

## CATEGORIA
- POST:
http://127.0.0.1:8000/api/catalogo/
JSON:
{
"nombre": "Procesadores",
"descripcion": "Se encarga de recibir, interpretar y ejecutar las instrucciones de los programas y del sistema operativo"
}

http://127.0.0.1:8000/api/catalogo/1/eliminado_logico/


- PUT:
http://127.0.0.1:8000/api/catalogo/1/
{
"nombre": "Procesador",
}

- GET:
http://127.0.0.1:8000/api/catalogo/categoria/
http://127.0.0.1:8000/api/catalogo/categoria/4/

## CATEGORIA ONLY READ
- GET:
http://127.0.0.1:8000/api/catalogo/categoria-get/
http://127.0.0.1:8000/api/catalogo/categoria-get/2/

## MARCA
- POST:
http://127.0.0.1:8000/api/catalogo/marca/
JSON:
{   
    "nombre":"Apple",
    "logo": "logo.com",
    "descripcion":"Lorem",
    "pais_origen":"Argentina"
}

http://127.0.0.1:8000/api/catalogo/marca/1/eliminado_logico/

- PUT:
{
"logo": "logo.com",
}

- GET:
http://127.0.0.1:8000/api/catalogo/marca/
http://127.0.0.1:8000/api/catalogo/marca/2/


## MARCA ONLY READ
- GET:
http://127.0.0.1:8000/api/catalogo/marca-get/
http://127.0.0.1:8000/api/catalogo/marca-get/2/

## PROVEEDOR
- POST:
http://127.0.0.1:8000/api/catalogo/proveedor/
JSON:
{
  "nombre":"Tecno Mayorista SRL",
  "cuit":"45-87125458-9",
  "email":"tecnomayoristasrl@gmaiñ.com",
  "telefono":"3587459657",
  "direccion":"San Luis 784"
}

http://127.0.0.1:8000/api/catalogo/proveedor/1/eliminado_logico/

- PUT:
http://127.0.0.1:8000/api/catalogo/proveedor/3/
JSON:
{
  "nombre":"Tecno Mayoristas SRL",
}

- GET:
http://127.0.0.1:8000/api/catalogo/proveedor/
http://127.0.0.1:8000/api/catalogo/proveedor/3/

## PROVEEDOR ONLY READ
- GET:
http://127.0.0.1:8000/api/catalogo/proveedor-get/
http://127.0.0.1:8000/api/catalogo/proveedor-get/3/


## PRODUCTO
- POST:
http://127.0.0.1:8000/api/catalogo/producto/
JSON:
{
    "nombre": "Teclado Mecánico RGB",
    "descripcion_corta": "Teclado mecánico con iluminación RGB",
    "descripcion_larga": "Teclado mecánico gamer con switches red, conexión USB y retroiluminación RGB personalizable.",
    "sku": "A001",
    "precio_lista": "85000.00",
    "precio_oferta": "74999.99",
    "stock_total": 25,
    "marca": 2,
    "categoria": 1
}


PUT:
http://127.0.0.1:8000/api/catalogo/producto/2/
{
    "destacado": false,
}

GET:
http://127.0.0.1:8000/api/catalogo/producto/
http://127.0.0.1:8000/api/catalogo/producto/2/

## PRODUCTO ONLY READ
GET:
http://127.0.0.1:8000/api/catalogo/producto-get/
http://127.0.0.1:8000/api/catalogo/producto-get/1/


## PRODUCTO_IMG


## COMPRA


## DETALLE COMPRA


## VENTA


## DETALLE VENTA
