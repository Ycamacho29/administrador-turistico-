import secrets
import uuid
import time


def generar_codigo_pago():
    caracteres = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return ''.join(secrets.choice(caracteres) for _ in range(8))


def generar_codigo_reserva() -> str:
    """
    Genera un código único para una reserva con el formato: RES-XXXX-XXXX
    Combina la marca de tiempo actual en base 36 y un fragmento de UUID.
    """
    # 1. Obtenemos el timestamp actual y lo convertimos a base 36 (alfanumérico corto)
    timestamp = int(time.time() * 1000)
    # Convertir a una cadena alfanumérica invertida de 4 caracteres
    time_part = hex(timestamp)[2:].upper()[-4:]

    # 2. Generamos un bloque aleatorio usando la entropía de UUID
    uuid_part = uuid.uuid4().hex[:4].upper()

    # 3. Estructuramos el código final
    return f"RES-{time_part}-{uuid_part}"
