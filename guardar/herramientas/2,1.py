import json
import os
import unicodedata

INVENTARIO_INICIAL = {
    "Camisa": {"precio": 45000, "stock": 20},
    "Gorra": {"precio": 30000, "stock": 5},
    "Pantalón": {"precio": 89000, "stock": 12},
    "Medias": {"precio": 8000, "stock": 40},
    "Zapatos": {"precio": 150000, "stock": 3},
}

if not os.path.exists("inventario.json"):
    with open("inventario.json", "w", encoding="utf-8") as archivo:
        json.dump(INVENTARIO_INICIAL, archivo, ensure_ascii=False, indent=2)

with open("inventario.json", "r", encoding="utf-8") as archivo:
    INVENTARIO = json.load(archivo)


def _limpiar_texto(texto: str) -> str:
    texto = texto.strip().lower()
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    if sin_tildes.endswith("es") and len(sin_tildes) > 4:
        sin_tildes = sin_tildes[:-2]
    elif sin_tildes.endswith("s") and len(sin_tildes) > 3:
        sin_tildes = sin_tildes[:-1]
    return sin_tildes


def buscar_producto(nombre: str):
    if not isinstance(nombre, str) or not nombre.strip():
        return None
    objetivo = _limpiar_texto(nombre)
    for prod in INVENTARIO:
        if _limpiar_texto(prod) == objetivo:
            return prod
    return None


def consultar_producto(nombre: str) -> dict:
    prod = buscar_producto(nombre)
    if prod is None:
        return {"existe": False, "precio": None, "stock": 0}
    datos = INVENTARIO[prod]
    return {
        "existe": True,
        "producto": prod,
        "precio": datos["precio"],
        "stock": datos["stock"],
    }


def calcular_envio(ciudad: str) -> int:
    if not isinstance(ciudad, str) or not ciudad.strip():
        raise ValueError("La ciudad de envío es obligatoria.")
    return 0 if _limpiar_texto(ciudad) == "popayan" else 13000


def calcular_descuento(subtotal: int | float) -> int:
    return int(round(subtotal * 0.15)) if subtotal > 300000 else 0


def calcular_pedido(items: list, ciudad: str) -> dict:
    if not isinstance(items, list) or len(items) == 0:
        raise ValueError("El pedido debe tener al menos un producto.")

    envio = calcular_envio(ciudad)
    subtotal = 0
    detalle = []

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Cada elemento de items debe ser un diccionario.")
        nombre = item["producto"]
        cantidad = item["cantidad"]

        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError(f"La cantidad de '{nombre}' debe ser un entero mayor que 0.")

        prod = buscar_producto(nombre)
        if prod is None:
            raise ValueError(f"El producto '{nombre}' no existe.")

        stock_actual = INVENTARIO[prod]["stock"]
        if cantidad > stock_actual:
            raise ValueError(
                f"Stock insuficiente para '{prod}': pedido {cantidad}, disponible {stock_actual}."
            )

        precio = INVENTARIO[prod]["precio"]
        importe = precio * cantidad
        subtotal += importe
        detalle.append({
            "producto": prod,
            "cantidad": cantidad,
            "precio_unitario": precio,
            "importe": importe,
        })

    descuento = calcular_descuento(subtotal)
    total = subtotal - descuento + envio

    return {
        "ciudad": ciudad,
        "items": detalle,
        "subtotal": subtotal,
        "descuento": descuento,
        "envio": envio,
        "total": total,
    }


if __name__ == "__main__":
    resultado = calcular_pedido(
        [
            {"producto": "pantalones", "cantidad": 2},
            {"producto": "zapatos", "cantidad": 1},
        ],
        "Cali",
    )
    print(resultado)