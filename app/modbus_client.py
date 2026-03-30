from pymodbus.client import ModbusTcpClient
from app.config import ESP32_IP, ESP32_PORT

# Direcciones Modbus
REG_TEMP_X10 = 0
REG_FOCO = 1
REG_MOTOR = 2


class ModbusController:
    def __init__(self, host=ESP32_IP, port=ESP32_PORT):
        self.host = host
        self.port = port

    def _client(self):
        return ModbusTcpClient(self.host, port=self.port)

    def get_temperature(self) -> float:
        client = self._client()
        try:
            client.connect()
            result = client.read_holding_registers(address=REG_TEMP_X10, count=1)

            if result.isError():
                raise RuntimeError("No fue posible leer la temperatura por Modbus")

            return result.registers[0] / 10.0

        finally:
            client.close()

    def set_foco(self, estado: bool) -> None:
        client = self._client()
        try:
            client.connect()
            value = 1 if estado else 0

            result = client.write_register(address=REG_FOCO, value=value)

            if result.isError():
                raise RuntimeError("No fue posible escribir el estado del foco")

        finally:
            client.close()

    def set_motor(self, estado: bool) -> None:
        client = self._client()
        try:
            client.connect()
            value = 1 if estado else 0

            result = client.write_register(address=REG_MOTOR, value=value)

            if result.isError():
                raise RuntimeError("No fue posible escribir el estado del motor")

        finally:
            client.close()