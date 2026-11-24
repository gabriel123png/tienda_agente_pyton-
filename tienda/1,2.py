import importlib.util
import json
import unicodedata
from pathlib import Path

_ruta_1_1 = Path(__file__).resolve().parent / "1,1.py"
_spec_1_1 = importlib.util.spec_from_file_location("modulo_1_1", _ruta_1_1)
_modulo_1_1 = importlib.util.module_from_spec(_spec_1_1)
_spec_1_1.loader.exec_module(_modulo_1_1)

MODELO = _modulo_1_1.MODELO
client = _modulo_1_1.client
herramientas = _modulo_1_1.herramientas
pedir_envio = _modulo_1_1.pedir_envio


def _limpiar(texto: str) -> str:
    texto = texto.strip().lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def calcular_envio(ciudad: str) -> int:
    return 0 if _limpiar(ciudad) == "popayan" else 13000


def responder_con_resultado():
    mensajes, respuesta = pedir_envio()

    mensajes.append({"role": "assistant", "content": respuesta.content})

    resultados = []
    for bloque in respuesta.content:
        if bloque.type == "tool_use" and bloque.name == "calcular_envio":
            valor = calcular_envio(bloque.input["ciudad"])
            resultados.append(
                {
                    "type": "tool_result",
                    "tool_use_id": bloque.id,
                    "content": json.dumps({"envio": valor}, ensure_ascii=False),
                }
            )

    mensajes.append({"role": "user", "content": resultados})

    respuesta_final = client.messages.create(
        model=MODELO,
        max_tokens=512,
        tools=herramientas,
        messages=mensajes,
    )

    texto_final = "\n".join(
        b.text for b in respuesta_final.content if b.type == "text"
    )
    print("Texto final:", texto_final)


if __name__ == "__main__":
    responder_con_resultado()