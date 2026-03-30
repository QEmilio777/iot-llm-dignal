from app.modbus_client import ModbusController


class ActionService:

    def __init__(self):
        self.modbus = ModbusController()

    def execute(self, llm_text: str) -> str:
        llm_text = llm_text.strip()

        if "ACCION=ENCENDER_FOCO" in llm_text:
            self.modbus.set_foco(True)
            return "Foco encendido correctamente."

        if "ACCION=APAGAR_FOCO" in llm_text:
            self.modbus.set_foco(False)
            return "Foco apagado correctamente."

        if "ACCION=ENCENDER_MOTOR" in llm_text:
            self.modbus.set_motor(True)
            return "Motor encendido correctamente."

        if "ACCION=APAGAR_MOTOR" in llm_text:
            self.modbus.set_motor(False)
            return "Motor apagado correctamente."

        if "ACCION=CONSULTAR_TEMPERATURA" in llm_text:
            temp = self.modbus.get_temperature()
            return f"La temperatura actual es de {temp:.1f} grados Celsius."

        if "ACCION=RESPONDER" in llm_text:
            for line in llm_text.splitlines():
                if line.startswith("MENSAJE="):
                    return line.replace("MENSAJE=", "", 1).strip()

            return "No se recibió un mensaje válido del modelo."

        return (
            "No fue posible interpretar la respuesta del modelo. "
            "Revise el prompt del sistema o el formato de salida."
        )