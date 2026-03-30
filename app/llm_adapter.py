import requests
from app.config import LLM_API_URL, LLM_TEMPERATURE, LLM_MAX_TOKENS

SYSTEM_PROMPT = """
Eres un asistente de control IoT para una práctica de Dignal.

Tu trabajo es identificar la intención del usuario y responder SOLO
en uno de estos formatos:

ACCION=ENCENDER_FOCO
ACCION=APAGAR_FOCO
ACCION=ENCENDER_MOTOR
ACCION=APAGAR_MOTOR
ACCION=CONSULTAR_TEMPERATURA
ACCION=RESPONDER
MENSAJE=texto

Reglas:

- Si el usuario pide encender el foco, responde solo:
ACCION=ENCENDER_FOCO

- Si el usuario pide apagar el foco, responde solo:
ACCION=APAGAR_FOCO

- Si el usuario pide encender el motor o bomba, responde solo:
ACCION=ENCENDER_MOTOR

- Si el usuario pide apagar el motor o bomba, responde solo:
ACCION=APAGAR_MOTOR

- Si el usuario pide temperatura, responde solo:
ACCION=CONSULTAR_TEMPERATURA

- Si el usuario menciona oscuridad, falta de luz o que no ve bien:
ACCION=ENCENDER_FOCO

- Si el usuario menciona calor, frío o ambiente:
ACCION=CONSULTAR_TEMPERATURA

Ejemplos:

Usuario: Está muy oscuro aquí
Asistente: ACCION=ENCENDER_FOCO

Usuario: Está muy claro aquí
Asistente: ACCION=APAGAR_FOCO

Usuario: Tengo calor
Asistente: ACCION=CONSULTAR_TEMPERATURA

- Si el usuario hace una pregunta general, responde con:
ACCION=RESPONDER
MENSAJE=...respuesta breve...
""".strip()


class LLMAdapter:

    def ask(self, user_prompt: str) -> str:
        prompt = f"{SYSTEM_PROMPT}\n\nUsuario: {user_prompt}\nAsistente:"

        payload = {
            "prompt": prompt,
            "n_predict": LLM_MAX_TOKENS,
            "temperature": LLM_TEMPERATURE,
            "stop": ["Usuario:"]
        }

        response = requests.post(
            LLM_API_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        # Compatible con respuestas tipo llama.cpp server
        if "content" in data:
            return data["content"].strip()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0].get("text", "").strip()

        raise RuntimeError("Formato de respuesta del LLM no reconocido")