HERRAMIENTAS = [
    {
        "name": "consultar_producto",
        "description": (
            "Consulta si un producto existe, su precio unitario y el stock disponible. "
            "Úsala cuando el usuario pregunte por precios, disponibilidad o existencias de un producto."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre": {
                    "type": "string",
                    "description": "Nombre del producto a consultar.",
                }
            },
            "required": ["nombre"],
        },
    },
    {
        "name": "calcular_pedido",
        "description": (
            "Calcula subtotal, descuento (15% si el subtotal pasa de 300000), envío "
            "(0 a Popayán, 13000 a otra ciudad) y total de un pedido validando stock. "
            "Úsala para calcular todos los totales de un pedido cuando se conozcan productos, cantidades y ciudad."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "description": "Lista de objetos con 'producto' y 'cantidad'.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "producto": {"type": "string"},
                            "cantidad": {"type": "integer"},
                        },
                        "required": ["producto", "cantidad"],
                    },
                },
                "ciudad": {
                    "type": "string",
                    "description": "Ciudad de envío del pedido.",
                },
            },
            "required": ["items", "ciudad"],
        },
    },
]