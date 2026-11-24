import os
from pathlib import Path
import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError(
        "Falta ANTHROPIC_API_KEY. Revisa el archivo .env en la carpeta tienda_agente "
        "o configura la variable de entorno ANTHROPIC_API_KEY."
    )

client = anthropic.Anthropic(api_key=api_key)
MODELO = "claude-sonnet-4-5"

herramientas = [
    {
        "name": "calcular_envio",
        "description": "Calcula el costo de envío: gratis (0) a Popayán y 13000 a cualquier otra ciudad.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ciudad": {
                    "type": "string",
                    "description": "Ciudad de destino del envío.",
                }
            },
            "required": ["ciudad"],
        },
    }
]


def pedir_envio():
    mensajes = [{"role": "user", "content": "¿Cuánto cuesta el envío a Cali?"}]
    respuesta = client.messages.create(
        model=MODELO,
        max_tokens=512,
        tools=herramientas,
        messages=mensajes,
    )

    print("stop_reason:", respuesta.stop_reason)
    for bloque in respuesta.content:
        if bloque.type == "tool_use":
            print("name:", bloque.name, "| input:", bloque.input)

    return mensajes, respuesta


if __name__ == "__main__":
    pedir_envio()