# Documentación API SPC Suplementos

## Autenticación

Todas las peticiones a la API deben incluir un token JWT en el header de autorización: 
```
Authorization: Bearer <token>
```

Para obtener un token, hacer una petición POST a `/api/token` con autenticación básica:
```bash
curl -X POST http://localhost:5000/api/token -u username:password
```

## Endpoints

### Productos

#### GET /api/productos
Obtiene lista de todos los productos activos.

Respuesta:
```json
[
    {
        "id": 1,
        "codigo": "P001",
        "nombre": "Producto 1",
        "precio_venta": 100.0,
        "stock": 10
    }
]
```

#### POST /api/productos
Crea un nuevo producto.

Request:
```json
{
    "codigo": "P001",
    "nombre": "Producto 1",
    "precio_costo": 80.0,
    "precio_venta": 100.0,
    "stock": 10
}
```

### Ventas

#### GET /api/ventas
Obtiene lista de ventas con filtros opcionales:
- fecha_desde
- fecha_hasta
- cliente_id

#### POST /api/ventas
Crea una nueva venta.

Request:
```json
{
    "cliente_id": 1,
    "items": [
        {
            "producto_id": 1,
            "cantidad": 2
        }
    ]
}
```

## Códigos de Error

- 400: Bad Request - Datos inválidos
- 401: Unauthorized - Token inválido o faltante
- 404: Not Found - Recurso no encontrado
- 500: Internal Server Error
```

Continuaré con más archivos y configuraciones...