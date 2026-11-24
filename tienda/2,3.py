import importlib.util
import json
from pathlib import Path

_ruta_2_1 = Path(__file__).resolve().parents[1] / "guardar" / "herramientas" / "2,1.py"
_spec_2_1 = importlib.util.spec_from_file_location("modulo_2_1", _ruta_2_1)
_modulo_2_1 = importlib.util.module_from_spec(_spec_2_1)
_spec_2_1.loader.exec_module(_modulo_2_1)

consultar_producto = _modulo_2_1.consultar_producto
calcular_pedido = _modulo_2_1.calcular_pedido

FUNCIONES = {
    "consultar_producto": lambda entrada: consultar_producto(**entrada),
    "calcular_pedido": lambda entrada: calcular_pedido(**entrada),
}


def ejecutar_herramienta(nombre: str, entrada: dict) -> tuple[str, bool]:
    if nombre not in FUNCIONES:
        return json.dumps({"error": f"La herramienta '{nombre}' no existe."}, ensure_ascii=False), True
    try:
        resultado = FUNCIONES[nombre](entrada)
        return json.dumps(resultado, ensure_ascii=False), False
    except (ValueError, KeyError, TypeError) as exc:
        return json.dumps({"error": str(exc)}, ensure_ascii=False), True


if __name__ == "__main__":
    texto_json, es_error = ejecutar_herramienta(
        "calcular_pedido",
        {
            "items": [
                {"producto": "pantalones", "cantidad": 2},
                {"producto": "zapatos", "cantidad": 1},
            ],
            "ciudad": "Cali",
        },
    )
    print("es_error:", es_error, "| texto:", texto_json)